from dataclasses import dataclass
from typing import Type

from loguru import logger

from griff.infrastructure.registry.endpoint_decorator_processor import (
    EndpointDecoratorProcessor,
)
from griff.infrastructure.registry.meta_registry import AbstractMetaRegistry
from griff.utils.get_decorators import get_decorators


@dataclass
class EndpointDefinition:
    endpoint: any
    http_method: str
    http_route: str
    http_success_code: int


class MetaEndpointControllerRegistry(AbstractMetaRegistry):
    ENDPOINT_REGISTRY = {}
    except_name = "AbstractEndpointController"

    def __new__(mcs, name, bases, attrs):
        new_cls = type.__new__(mcs, name, bases, attrs)

        if name == mcs.except_name:
            return new_cls

        for key, val in attrs.items():
            if key not in [
                "__module__",
                "__qualname__",
                "base_route",
                "router",
                "__classcell__",
                "__init__",
            ]:
                deco_list = get_decorators(val)

                if deco_list is None or len(deco_list) == 0:
                    continue

                decorator_processor = EndpointDecoratorProcessor()
                decorator_processor.load_decorators(deco_list)

                endpoint_def = EndpointDefinition(
                    endpoint=str(val).split(".")[1].split(" ")[0],
                    http_method=decorator_processor.method,
                    http_route=decorator_processor.route,
                    http_success_code=decorator_processor.code,
                )
                mcs.add_endpoint_to_controller(
                    endpoint=endpoint_def, controller=new_cls
                )

        return new_cls

    @classmethod
    def add_endpoint_to_controller(mcs, endpoint: EndpointDefinition, controller: Type):
        if controller not in mcs.ENDPOINT_REGISTRY.keys():
            mcs.ENDPOINT_REGISTRY[controller] = list()

        if endpoint not in mcs.ENDPOINT_REGISTRY[controller]:
            mcs.ENDPOINT_REGISTRY[controller].append(endpoint)
            logger.debug(f"{endpoint} definition appended to {controller}")

    @classmethod
    def get_endpoint_registry(mcs):
        return mcs.ENDPOINT_REGISTRY

    @classmethod
    def get_full_route_for_endpoint(cls, controller, endpoint: EndpointDefinition):
        if controller.base_route is None:
            return None
        base_route = controller.base_route.strip("/")
        if endpoint.http_route is None:
            return None
        endpoint_route = endpoint.http_route.strip("/")
        if base_route == "":
            return f"/{endpoint_route.strip('/')}"

        fullroute = f"/{base_route}/{endpoint_route}"
        return fullroute
