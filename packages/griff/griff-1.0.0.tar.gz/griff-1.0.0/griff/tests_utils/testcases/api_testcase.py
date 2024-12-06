from pprint import pprint
from typing import Optional, Union
from urllib.parse import urlencode

import orjson
from fastapi import Response, status
from httpx import AsyncClient
from pydantic import BaseModel, Field, field_validator, model_validator

from griff.runtime.runtime_factory import RuntimeFactory
from griff.tests_utils.mixins.runtime_test_mixin import RuntimeTestMixin
from griff.tests_utils.testcases.abstract_testcase import AbstractTestCase


class ApiClientParams(BaseModel):
    data_json: Optional[Union[list, dict]] = Field(None, alias="json")
    data: Optional[Union[list, dict]] = Field(None, alias="data")
    files: Optional[dict] = None
    auto_auth: bool = True
    access_token: Optional[str] = None
    headers: Optional[dict] = None

    @model_validator(mode="after")
    def check_auto_auth(cls, values):
        if values.auto_auth and values.access_token is None:
            raise ValueError("Missing Jwt Access Token for automatic authentication")
        return values

    @field_validator("headers")
    @classmethod
    def set_header(cls, value):
        return value or {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.auto_auth:
            self.headers["Authorization"] = f"Bearer {self.access_token}"

    def to_method_kwargs(self) -> dict:
        kwargs = super().dict(
            exclude={"auto_auth", "access_token"}, by_alias=True, exclude_none=True
        )
        if "json" in kwargs:
            # todofsc: create a Json Service
            kwargs["json"] = AbstractTestCase.to_json_dumpable(kwargs["json"])
        if "data" in kwargs:
            # todofsc: create a Json Service
            kwargs["data"] = AbstractTestCase.to_json_dumpable(kwargs["data"])
        return kwargs


# noinspection PyMethodOverriding
class FastApiTestClient(AsyncClient):
    default_access_token: str = None

    # noinspection PyMethodOverriding
    async def post(
        self,
        url,
        json: Optional[Union[list, dict]] = None,
        data: Optional[Union[list, dict]] = None,
        files: Optional[dict] = None,
        auto_auth: bool = False,
        access_token=None,
        headers: dict = None,
    ) -> Response:
        params = ApiClientParams(
            json=json,
            data=data,
            files=files,
            auto_auth=auto_auth,
            headers=headers,
            access_token=access_token if access_token else self.default_access_token,
        ).to_method_kwargs()
        return await super().post(url=url, **params)

    async def get(
        self,
        url,
        auto_auth: bool = True,
        access_token=None,
        headers: dict = None,
    ) -> Response:
        params = ApiClientParams(
            auto_auth=auto_auth,
            headers=headers,
            access_token=access_token if access_token else self.default_access_token,
        ).to_method_kwargs()
        return await super().get(url=url, **params)

    async def put(
        self,
        url,
        json: Optional[Union[list, dict]] = None,
        files: Optional[dict] = None,
        auto_auth: bool = True,
        access_token=None,
        headers: dict = None,
    ) -> Response:
        params = ApiClientParams(
            json=json,
            files=files,
            auto_auth=auto_auth,
            headers=headers,
            access_token=access_token if access_token else self.default_access_token,
        ).to_method_kwargs()
        return await super().put(url=url, **params)

    async def patch(
        self,
        url,
        json: Optional[Union[list, dict]] = None,
        files: Optional[dict] = None,
        auto_auth: bool = True,
        access_token=None,
        headers: dict = None,
    ) -> Response:
        params = ApiClientParams(
            json=json,
            files=files,
            auto_auth=auto_auth,
            headers=headers,
            access_token=access_token if access_token else self.default_access_token,
        )
        return await super().patch(url=url, **params.to_method_kwargs())

    async def delete(
        self,
        url,
        auto_auth: bool = True,
        access_token=None,
        headers: dict = None,
    ) -> Response:
        params = ApiClientParams(
            auto_auth=auto_auth,
            headers=headers,
            access_token=access_token if access_token else self.default_access_token,
        ).to_method_kwargs()
        return await super().delete(url=url, **params)


class ApiTestCase(RuntimeTestMixin, AbstractTestCase):
    bounded_context: str = None
    runtime_factory_class: RuntimeFactory = None

    @classmethod
    def build_runtime_factory(cls):
        return cls.runtime_factory_class().test_api_runtime(
            bounded_context=cls.bounded_context
        )

    @classmethod
    def init_class_context_data(cls):
        pass

    @classmethod
    def init_class_context_services(cls):
        pass

    def init_method_context_data(self):
        pass

    def init_method_context_services(self):
        pass

    async def async_setup(self):
        await super().async_setup()
        self.app = self.get_runtime().get_fast_api()
        self.client = FastApiTestClient(app=self.app, base_url="http://test")

    def assert_response_equals_resultset(
        self, response: Response, remove_paths: Optional[list] = None
    ):
        return self.assert_equals_resultset(
            self.prepare_response_for_resultset(response), remove_paths=remove_paths
        )

    def assert_response_status_code(
        self, response: Response, status=status.HTTP_200_OK
    ):
        assert status == response.status_code, (
            f"expected status {status} got {response.status_code}\n"
            f"response body: {self.get_response_body(response)}"
        )

    @classmethod
    def prepare_response_for_resultset(cls, response: Response):
        try:
            return {
                "status_code": response.status_code,
                "body": cls.get_response_body(response),
            }
        except Exception as e:
            pprint(cls.get_response_body(response))
            raise e

    def list_api_routes(self, api_name, except_routes: list = None):
        if except_routes is None:
            except_routes = []
        return [
            route
            for route in self.app.routes
            if f"{api_name}:" in route.name and route.name not in except_routes
        ]

    def reverse_url(self, name, query_kwargs=None, **kwargs):
        """
        Url reverse from FastAPI routes

        Usage:
            reverse(
                <url_name>,
                pk=123,
                query_kwargs={'key':'value', 'k2': 'v2'}
            )
            => url/123?key=value&k2=v2

        Args:
            name: route name
            query_kwargs: optional query params
            **kwargs: route url params

        Returns:
            str: relative url built from router name and params with query params
            if asked
        """
        base_url = self.app.url_path_for(name, **kwargs)
        if query_kwargs:
            return f"{base_url}?{urlencode(query_kwargs, doseq=True)}"

        return base_url

    @classmethod
    def get_response_body(cls, response: Response):
        return orjson.loads(response.content) if response.content else None
