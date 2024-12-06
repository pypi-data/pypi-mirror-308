from abc import ABC

from pydantic import BaseModel

from griff.infrastructure.bus.query.abstract_query import QueryResponsePagination


class AbstractSchema(BaseModel, ABC):
    ...


class AbstractPaginationSchema(BaseModel, ABC):
    pagination: QueryResponsePagination | None = None


class AbstractCreateSchema(BaseModel):
    ...


class AbstractHydrateSchema(BaseModel):
    ...
