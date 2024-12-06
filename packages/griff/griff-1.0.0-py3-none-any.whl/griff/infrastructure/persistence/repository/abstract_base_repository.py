from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from injector import inject

from griff.domain.auto_vo.abstract_aggregate_root import (
    AbstractAggregateFactory,
    AbstractAggregateRoot,
)
from griff.domain.common_domain_exceptions import AggregatePersistenceError
from griff.exceptions import EntityNotFoundError
from griff.infrastructure.persistence.repository.persistence_adapter.abstract_persistence_adapter import (  # noqa
    AbstractPersistenceAdapter,
)
from griff.services.date.date_service import DateService
from griff.services.json.json_service import JsonService

A = TypeVar("A", bound=AbstractAggregateRoot)


class AbstractBaseRepository(Generic[A], ABC):
    @inject
    @abstractmethod
    def __init__(
        self,
        aggregate_factory: AbstractAggregateFactory,
        persistance_adapter: AbstractPersistenceAdapter,
        date_service: DateService,
    ):
        self._date_service = date_service
        self._factory = aggregate_factory
        self._persistance_adapter = persistance_adapter

    def _check_aggregate(self, aggregate: A):
        if not aggregate.is_valid():
            self.raise_persistence_error(
                "Aggregate is not valid, persistence forbidden",
                details={
                    "aggregate_type": self._factory.aggregate_type.__name__,
                    "errors": aggregate.get_validation_errors(),
                },
            )

    def _add_persistence_metadata_for_creation(
        self, target_dict: dict[str, Any]
    ) -> dict[str, Any]:
        now = self._date_service.now().to_datetime()
        target_dict["created_at"] = now
        target_dict["updated_at"] = now
        return target_dict

    def _add_persistence_metadata_for_update(
        self, target_dict: dict[str, Any]
    ) -> dict[str, Any]:
        now = self._date_service.now().to_datetime()
        target_dict["updated_at"] = now
        return target_dict

    def serialize_for_persistence(self, aggregate: A) -> dict[str, Any]:
        return aggregate.to_dict()

    def add_creation_extra_data(self, target_dict: dict[str, Any]) -> dict[str, Any]:
        return target_dict

    def add_update_extra_data(self, target_dict: dict[str, Any]) -> dict[str, Any]:
        return target_dict

    def _convert_to_hydratation_dict(self, results: dict) -> dict:
        return results

    def _hydrate_aggregate(self, results: dict) -> A:
        aggregate = self._factory.hydrate(results)

        if aggregate.is_valid() is False:
            self.raise_persistence_error(
                "Aggregate is not valid, hydratation impossible",
                details={
                    "aggregate_type": self._factory.aggregate_type.__name__,
                    "errors": aggregate.get_validation_errors(),
                },
            )

        return aggregate

    async def add(self, aggregate: A):
        self._check_aggregate(aggregate)
        agg_dict = self.serialize_for_persistence(aggregate)
        updated_dict = self._add_persistence_metadata_for_creation(agg_dict)
        updated_dict = self.add_creation_extra_data(updated_dict)
        try:
            results = await self._persistance_adapter.persist_new(updated_dict)
        except (RuntimeError, ValueError) as e:
            self.raise_persistence_error(e.args[0], {"entity_id": aggregate.entity_id})
        return results

    async def update(self, aggregate: A):
        self._check_aggregate(aggregate)
        agg_dict = self.serialize_for_persistence(aggregate)
        updated_dict = self._add_persistence_metadata_for_update(agg_dict)
        updated_dict = self.add_update_extra_data(updated_dict)
        try:
            results = await self._persistance_adapter.persist_existing(updated_dict)
        except ValueError as e:
            self.raise_persistence_error(e.args[0], {"entity_id": aggregate.entity_id})
        if results is None:
            self.raise_persistence_error(
                message="impossible to update aggregate",
                details={
                    "aggregate_type": self._factory.aggregate_type.__name__,
                    "entity_id": aggregate.entity_id,
                },
            )
        return results

    async def add_or_update(self, aggregate):
        existing_aggregate = await self._get_by_id(aggregate.entity_id)
        if existing_aggregate:
            return await self.update(aggregate)
        return await self.add(aggregate)

    async def get_by_id(self, entity_id: str) -> A:
        result = await self._get_by_id(entity_id)
        if result is None:
            raise EntityNotFoundError(
                f"{self._aggregate_class()} '{entity_id}' not found",
                {"entity_id": entity_id},
            )
        return self._hydrate_result(result)

    async def get_by_query(self, query_name: str, **query_params) -> A:
        result = await self._get_by_query(query_name, **query_params)
        if result is None:
            raise EntityNotFoundError(
                f"{self._aggregate_class()} not found", query_params
            )
        return self._hydrate_result(result)

    def _hydrate_result(self, result: dict) -> A:
        raw_data = self._convert_to_hydratation_dict(result)
        return self._hydrate_aggregate(raw_data)

    def raise_persistence_error(self, message: str, details: dict = None) -> None:
        raise AggregatePersistenceError(message, details=details)

    async def delete(self, aggregate: A):
        self._check_aggregate(aggregate)
        try:
            await self.get_by_id(aggregate.entity_id)
            await self._persistance_adapter.remove_from_persistence(aggregate.entity_id)
        except (RuntimeError, ValueError, EntityNotFoundError) as e:
            self.raise_persistence_error(e.args[0], {"entity_id": aggregate.entity_id})

    async def _get_by_id(self, entity_id: str) -> dict | None:
        try:
            return await self._persistance_adapter.get_from_persistence(entity_id)
        except ValueError:
            return None

    async def _get_by_query(self, query_name: str, **query_params: dict) -> dict:
        try:
            return await self._persistance_adapter.run_query(query_name, **query_params)
        except ValueError:
            return None

    def _aggregate_class(self):
        return self._factory.aggregate_type.__name__


class AbstractSerializedRepository(AbstractBaseRepository[A], ABC):
    @inject
    @abstractmethod
    def __init__(
        self,
        aggregate_factory: AbstractAggregateFactory,
        persistance_adapter: AbstractPersistenceAdapter,
        date_service: DateService,
        json_service: JsonService,
    ):
        super().__init__(aggregate_factory, persistance_adapter, date_service)
        self._json_service = json_service

    def serialize_for_persistence(self, aggregate: A) -> dict[str, Any]:
        return {
            "entity_id": aggregate.entity_id,
            "serialized": self._get_serialized(aggregate),
        }

    def _get_serialized(self, aggregate: A) -> str:
        json_prepared = self._json_service.to_json_dumpable(aggregate.to_dict())
        return self._json_service.dump(json_prepared)

    def _convert_to_hydratation_dict(self, results: dict) -> dict:
        return self._json_service.load_from_str(results["serialized"])
