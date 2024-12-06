import abc

from injector import inject, singleton

from griff.infrastructure.persistence.repository.persistence_adapter.abstract_persistence_adapter import (  # noqa
    AbstractPersistenceAdapter,
)
from griff.services.query_runner.query_runner_service import QueryRunnerService


@singleton
class DbPersistenceAdapter(AbstractPersistenceAdapter, abc.ABC):
    @inject
    def __init__(self, query_service: QueryRunnerService):
        self._query_service = query_service
        self._query_service.set_sql_queries(self._get_relative_sql_queries_path())

    async def persist_new(self, raw_data: dict) -> str:
        entity_id = await self._query_service.run_query(query_name="insert", **raw_data)
        return entity_id

    async def persist_existing(self, raw_data: dict) -> str:
        results = await self._query_service.run_query(query_name="update", **raw_data)
        return results

    async def remove_from_persistence(self, persistence_id: str) -> None:
        results = await self._query_service.run_query(
            query_name="delete", entity_id=persistence_id
        )
        return results

    async def get_from_persistence(self, persistence_id: str) -> dict:
        results = await self._query_service.run_query(
            query_name="get_by_id", entity_id=persistence_id
        )
        return results

    async def list_all(self) -> list[dict]:
        results = await self._query_service.run_query(query_name="list_all")
        return results

    async def run_query(self, query_name: str, **query_params):
        return await self._query_service.run_query(query_name, **query_params)

    async def list_with_predicate(self, predicate) -> list[dict]:
        pass

    @classmethod
    @abc.abstractmethod
    def _get_relative_sql_queries_path(cls) -> str:
        """get relative queries path"""
        ...
