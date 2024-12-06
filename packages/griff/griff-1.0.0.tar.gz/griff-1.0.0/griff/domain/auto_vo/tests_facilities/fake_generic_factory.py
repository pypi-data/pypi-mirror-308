from griff.domain.auto_vo.generic_factory import (
    GenericAggregateFactoryCompanion,
    GenericEntityFactory,
)
from griff.domain.auto_vo.tests_facilities.aggregates_test_mixin import _TestRulesPack


class FakeGenericEntityFactory(GenericEntityFactory):
    def __init__(self, _companion: GenericAggregateFactoryCompanion, services: list):
        super().__init__(_companion=_companion, services=services)

    def build(self, **kwargs):
        pass

    def hydrate(self, **kwargs):
        pass

    @property
    def aggregate_type(self) -> type:
        return _TestRulesPack
