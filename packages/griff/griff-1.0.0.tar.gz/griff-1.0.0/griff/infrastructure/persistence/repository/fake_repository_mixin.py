from typing import List, Optional

from griff.domain.auto_vo.abstract_aggregate_root import AbstractAggregateRoot


class FakeRepositoryMixin:
    # noinspection PyMissingConstructor
    def __init__(self, **kwargs):
        self._aggregates = list()

    def init_repository(self, aggregates=List[AbstractAggregateRoot]):
        self._aggregates = list(aggregates)

    def set_bad_format_exception_type(self, bad_format_exception_type: type):
        self._bad_format_exc = bad_format_exception_type

    def set_not_found_exception_type(self, not_found_exception_type: type):
        self._not_found_exc = not_found_exception_type

    async def add(self, aggregate: AbstractAggregateRoot):
        self._aggregates.append(aggregate)

    async def get_by_id(self, entity_id) -> Optional[AbstractAggregateRoot]:
        for aggregate in self._aggregates:
            if aggregate.entity_id == entity_id:
                return aggregate
        raise self._not_found_exc(f"{entity_id} not found in fake repository")

    async def get_by_field(self, field_name: str, field_value: str):
        for aggregate in self._aggregates:
            if getattr(aggregate, field_name) == field_value:
                return aggregate
        raise self._not_found_exc(
            f"{field_value} not found for {field_name} in fake repository"
        )
