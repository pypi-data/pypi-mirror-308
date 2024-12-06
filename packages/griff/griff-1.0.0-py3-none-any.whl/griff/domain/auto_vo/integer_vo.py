from griff.domain.auto_vo.base_value_object import AbstractConstraint, BaseValueObject
from griff.domain.auto_vo.constraints.base_constraint.integer import IntegerConstraint


class IntegerVo(BaseValueObject):
    def __init__(
        self,
        value: int,
        services: list = None,
        constraints: list[AbstractConstraint] = None,
    ):
        super().__init__(services=services, constraints=constraints)
        self._insert_type_constraint(IntegerConstraint())
        self._set_value(value)
