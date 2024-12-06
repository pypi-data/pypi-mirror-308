from griff.domain.auto_vo.base_value_object import AbstractConstraint, BaseValueObject
from griff.domain.auto_vo.constraints.base_constraint.string import StringConstraint
from griff.domain.auto_vo.constraints.in_enum import InEnum


class EnumVo(BaseValueObject):
    def __init__(
        self,
        value: str = None,
        services: list = None,
        constraints: list[AbstractConstraint] = list(),
    ):
        super().__init__(services=services, constraints=constraints)
        self._insert_type_constraint(StringConstraint())
        self.enum_type = self._get_enum_type()
        self._set_value(value)

    def _get_enum_type(self):
        for constraint in self._constraints:
            if isinstance(constraint, InEnum):
                return constraint.enum_type

    def _set_value(self, a_value) -> None:
        if self._value is not None:
            raise AttributeError("value object already set, modification forbidden")
        if type(a_value) is self.enum_type:
            self._value = a_value
            return
        if self._check_constraints(value_to_check=a_value):
            if type(a_value) is str:
                self._value = self.enum_type[a_value]

    @property
    def value(self):
        return self._value

    def to_dict(self) -> dict:
        return str(self._value)
