from griff.domain.auto_vo.base_value_object import AbstractConstraint, BaseValueObject
from griff.domain.auto_vo.constraints.base_constraint.string import StringConstraint


class StringVo(BaseValueObject):
    def __init__(
        self,
        value: str,
        services: list = None,
        constraints: list[AbstractConstraint] = list(),
    ):
        super().__init__(services=services, constraints=constraints)
        self._insert_type_constraint(StringConstraint())
        self._set_value(value)
