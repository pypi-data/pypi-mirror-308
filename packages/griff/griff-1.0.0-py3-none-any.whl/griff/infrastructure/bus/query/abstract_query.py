from abc import ABC, abstractmethod
from typing import Any, Type

from injector import inject
from pydantic import BaseModel, computed_field

from griff import exceptions
from griff.infrastructure.bus.command.abstract_command import PermissionMixin
from griff.infrastructure.registry.meta_registry import MetaQueryHandlerRegistry
from griff.services.query_runner.query_runner_service import QueryRunnerService


class QueryPagination(BaseModel):
    limit: int
    page: int = 1

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit

    @property
    def query_params(self) -> dict[str, int]:
        return {"limit": self.limit, "offset": self.offset}


class AbstractQuery(PermissionMixin, ABC):
    @abstractmethod
    def to_history(self) -> dict[str, Any]:
        return self.model_dump()

    @classmethod
    def get_name(cls) -> str:
        return cls.__name__

    @classmethod
    def get_type(cls) -> str:
        return "QUERY"


class AbstractGetByIdQuery(AbstractQuery, ABC):
    entity_id: str


class AbstractListQuery(AbstractQuery, ABC):
    pagination: QueryPagination | None = None


class AbstractListAllQuery(AbstractListQuery, ABC):
    ...


class AbstractQueryResponse(BaseModel, ABC):
    """
    AbstractQueryResponse is deprecated use QueryResponse directly
    """

    code: int
    msg: str
    value: Any


class QueryResponse(BaseModel, ABC):
    code: int
    msg: str
    value: Any


class QueryResponsePagination(BaseModel):
    total: int
    limit: int
    current_page: int

    @computed_field
    @property
    def next_page(self) -> int | None:
        next_page = self.current_page + 1
        if next_page <= self.nb_pages:
            return next_page
        return None

    @computed_field
    @property
    def previous_page(self) -> int | None:
        previous_page = self.current_page - 1
        if previous_page > 0:
            return previous_page
        return None

    @computed_field
    @property
    def nb_pages(self) -> int:
        return (
            self.total // self.limit + 1
            if self.total % self.limit
            else self.total // self.limit
        )


class AbstractQueryHandler(ABC, metaclass=MetaQueryHandlerRegistry):
    @inject
    def __init__(self, query_runner_service: QueryRunnerService):
        self._query_runner = query_runner_service
        self._query_runner.set_sql_queries(self._get_relative_sql_queries_path())

    @abstractmethod
    async def handle(self, query: AbstractQuery) -> QueryResponse:
        pass

    @classmethod
    @abstractmethod
    def listen_to(cls) -> Type[AbstractQuery]:
        pass

    @classmethod
    @abstractmethod
    def _get_relative_sql_queries_path(cls) -> str:
        """get relative queries path"""
        ...

    @staticmethod
    def _prepare_results(results: Any) -> Any:
        return results


class AbstractGetQueryHandler(AbstractQueryHandler, ABC):
    async def handle(self, query: AbstractGetByIdQuery) -> QueryResponse:
        query_params = query.model_dump(exclude={"required_permission"})
        results = await self._query_runner.run_query(
            self._get_query_name(), **query_params
        )
        if results:
            return QueryResponse(
                code=200, msg="entity found", value=self._prepare_results(results)
            )

        raise exceptions.EntityNotFoundError(details=query_params)

    @abstractmethod
    def _get_query_name(self) -> str:
        ...


class AbstractListQueryHandler(AbstractQueryHandler, ABC):
    async def handle(self, query: AbstractListQuery) -> QueryResponse:
        query_params = query.model_dump(exclude={"required_permission", "pagination"})
        pagination_query_params = {}
        if query.pagination is not None:
            pagination_query_params.update(query.pagination.query_params)
        results = await self._query_runner.run_query(
            self._get_query_name(), **{**query_params, **pagination_query_params}
        )
        if results is None:
            results = []
        results = self._prepare_results(results)
        if query.pagination:
            total = await self._query_runner.run_query(
                f"total_{self._get_query_name()}", **query_params
            )

            results = {
                "results": results,
                "pagination": QueryResponsePagination(
                    total=total,
                    limit=query.pagination.limit,
                    current_page=query.pagination.page,
                ),
            }

        msg = "entities found" if results else "no entities found"
        return QueryResponse(code=200, msg=msg, value=results)

    @abstractmethod
    def _get_query_name(self) -> str:
        ...


class AbstractGetByIdQueryHandler(AbstractGetQueryHandler, ABC):
    def _get_query_name(self) -> str:
        return "get_by_id"


class AbstractListAllQueryHandler(AbstractListQueryHandler, ABC):
    def _get_query_name(self) -> str:
        return "list_all"
