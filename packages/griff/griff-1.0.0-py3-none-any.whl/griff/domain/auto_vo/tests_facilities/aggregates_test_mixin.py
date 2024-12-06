from typing import Annotated, Any

from injector import inject

from griff.domain.abstract_entity import AbstractEntity
from griff.domain.auto_vo._tests.manual_vo_name import ManualTestNameVo
from griff.domain.auto_vo.abstract_aggregate_root import (
    AbstractAggregateFactory,
    AbstractAggregateRoot,
)
from griff.domain.auto_vo.constraints.length import MaxLength, MinLength
from griff.domain.auto_vo.constraints.min_max import MaxValue, MinValue
from griff.domain.auto_vo.constraints.positive import Positive
from griff.domain.auto_vo.constraints.required import Required
from griff.domain.auto_vo.integer_vo import IntegerVo
from griff.domain.auto_vo.string_vo import StringVo
from griff.domain.business_invariant_decorator import business_invariant
from griff.domain.value_object import ValueObject
from griff.infrastructure.bus.event.abstract_event import AbstractDomainEvent
from griff.services.date.date_service import DateService
from griff.services.uuid.uuid_service import UuidService

TestTypeVo = Annotated[IntegerVo, Positive()]
BonusPointVo = Annotated[IntegerVo, Positive(), Required()]


class _TestRulesPackCreatedEvent(AbstractDomainEvent):
    def to_history(self) -> dict[str, Any]:
        return super().to_history()


class BonusPointEntity(AbstractEntity):
    _td_bonus_point: BonusPointVo
    _cas_bonus_point: BonusPointVo
    _foul_bonus_point: BonusPointVo


@inject
class _TestRulesPackFactory(AbstractAggregateFactory):
    @inject
    def __init__(self, uuid_service: UuidService, date_service: DateService):
        aggregate_factory = _TestRulesPack.factory(
            services=[date_service, uuid_service]
        )
        super().__init__(aggregate_factory)


class _TestRulesPack(AbstractAggregateRoot):
    _name: Annotated[ManualTestNameVo, Required(), MinLength(3), MaxLength(75)]
    _win_point: TestTypeVo = None
    _draw_point: TestTypeVo
    _lose_point: TestTypeVo
    _bonus_points: Annotated[BonusPointEntity, Required()]

    def add_creation_event(self):
        return self.add_event(_TestRulesPackCreatedEvent)

    @business_invariant(name="Win point gt draw point")
    def _check_win_point_gt_draw_point(self):
        if self._win_point is None or self._draw_point is None:
            return True
        return self._win_point.value > self._draw_point.value


class _TestStartingPack(AbstractAggregateRoot):
    name: Annotated[ManualTestNameVo, Required(), MinLength(3), MaxLength(75)]
    free_skill: Annotated[IntegerVo, Positive(), Required()]
    draw_point: TestTypeVo
    lose_point: TestTypeVo

    def add_creation_event(self):
        pass


class FranchiseVO(ValueObject):
    _franchise_type: Annotated[str, Required(), MinLength(1), MaxLength(1)]
    _franchise_amount: Annotated[int, Required(), MaxValue(100), MinValue(0)]

    @property
    def value(self):
        return f"{self._franchise_amount}, {self._franchise_type}"


class _TestAggWithComplexVo(AbstractAggregateRoot):
    _simple_vo: Annotated[StringVo, Required(), MinLength(2)]
    _franchise_amount: Annotated[FranchiseVO, Required()]

    def add_creation_event(self):
        pass

    @property
    def franchise(self):
        return self._franchise_amount.value


class _TestRequired(AbstractAggregateRoot):
    simple_field: StringVo
    free_skill: Annotated[IntegerVo, Positive(), Required()]

    def a_sample_method_that_does_nothing(self, param1: int, param2: int):
        return param1 + param2

    def add_creation_event(self):
        pass


class MissingPrimaryId(AbstractAggregateRoot):
    simple_field: StringVo
    free_skill: Annotated[IntegerVo, Positive(), Required()]

    def add_creation_event(self):
        pass
