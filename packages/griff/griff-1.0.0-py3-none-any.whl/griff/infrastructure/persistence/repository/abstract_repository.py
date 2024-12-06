from abc import ABC
from typing import Any, Generic, TypeVar

from typing_extensions import deprecated

from griff.domain.auto_vo.abstract_aggregate_root import AbstractAggregateRoot
from griff.domain.auto_vo.generic_factory import GenericEntityFactory
from griff.domain.common_domain_exceptions import (
    AggregateHydratationError,
    AggregatePersistenceError,
    RepositoryActionUndefinedError,
)
from griff.services.date.date_service import DateService
from griff.services.query_runner.query_runner_service import QueryRunnerService

A = TypeVar("A", bound=AbstractAggregateRoot)


@deprecated("Use AbstractBaseRepository instead")
class AbstractRepository(Generic[A], ABC):
    """
    deprecated Use AbstractBaseRepository instead
    """

    def __init__(
        self,
        query_service: QueryRunnerService,
        date_service: DateService,
        aggregate_factory: GenericEntityFactory,
        query_dict: dict,
    ):
        self._identity_map = {}
        self._query_service = query_service
        self._date_service = date_service
        self._factory = aggregate_factory
        self._bad_format_exc = RuntimeError
        self._not_found_exc = ValueError
        self._query_dict = query_dict

    def to_db_data(self, aggregate: A) -> dict[str, Any]:
        return aggregate.to_dict()

    def get_query_name(self, action_name: str):
        if action_name not in self._query_dict.keys():
            exc = RepositoryActionUndefinedError()
            exc.details = {
                "action_name": action_name,
                "repository_type": self.__class__,
            }
            raise exc
        return self._query_dict[action_name]

    async def add(self, aggregate: A):
        if not aggregate.is_valid():
            exc = AggregatePersistenceError()
            exc.details = {
                "aggregate_type": self._factory.aggregate_type,
                "errors": aggregate.get_validation_errors(),
            }
            raise exc

        query_name = self.get_query_name("add")

        agg_dict = self.to_db_data(aggregate)
        now = self._date_service.now().to_datetime()
        agg_dict["created_at"] = now
        agg_dict["updated_at"] = now
        results = await self.get_query_service().run_query(
            query_name=query_name, **agg_dict
        )
        return results

    async def update(self, aggregate: A):
        if not aggregate.is_valid():
            exc = AggregatePersistenceError()
            exc.details = {
                "aggregate_type": self._factory.aggregate_type,
                "errors": aggregate.get_validation_errors(),
            }
            raise exc

        query_name = self.get_query_name("update")

        agg_dict = self.to_db_data(aggregate)
        agg_dict["updated_at"] = self._date_service.now().to_datetime()
        results = await self.get_query_service().run_query(
            query_name=query_name, **agg_dict
        )
        if results is None:
            raise self._not_found_exc()
        return results

    def get_query_service(self):
        return self._query_service

    def get_date_service(self):
        return self._date_service

    def _aggregate_from_results(self, results: dict) -> A:
        if results is None:
            raise self._not_found_exc()

        found_aggregate = self._factory.hydrate(results)

        if found_aggregate.is_valid() is False:
            exc = AggregateHydratationError()
            exc.details = {
                "aggregate_type": self._factory.aggregate_type(),
                "errors": found_aggregate.get_validation_errors(),
            }
            raise exc

        return found_aggregate

    async def get_by_id(self, entity_id: str) -> A:
        query_name = self.get_query_name("get_by_id")

        results = await self.get_query_service().run_query(
            query_name=query_name, entity_id=entity_id
        )

        if results is None:
            raise self._not_found_exc()

        return self._aggregate_from_results(results)

    async def get_by_field(self, field_name: str, field_value: str):
        query_name = self.get_query_name("get_by_field")
        kwargs = {field_name: field_value}
        results = await self.get_query_service().run_query(
            query_name=query_name, **kwargs
        )
        return self._aggregate_from_results(results)
