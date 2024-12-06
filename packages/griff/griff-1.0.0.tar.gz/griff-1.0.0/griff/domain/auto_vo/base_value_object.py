from typing import Any

from griff.domain.auto_vo.constraints.abstract_constraint import AbstractConstraint
from griff.domain.auto_vo.constraints.required import Required
from griff.domain.serializable import Serializable
from griff.domain.type_infos import TypeInfos
from griff.domain.validable import Validable
from griff.domain.with_business_invariant import WithBusinessInvariant


class BaseValueObject(Validable, Serializable, WithBusinessInvariant):
    def __init__(
        self,
        services: list = None,
        constraints: list[AbstractConstraint] = None,
    ):
        super().__init__()
        self._value = None
        self._constraints = constraints
        self._services = services
        if constraints is None:
            self._constraints = list()

    @property
    def value(self):
        return self._value

    def __eq__(self, other) -> Any:
        if not isinstance(other, self.__class__):
            return self.value == other
        return self.value == other.value

    def __str__(self):
        return f"{self._value}"

    def _get_service_of_type(self, service_type: type) -> any:
        if self._services is None or len(self._services) == 0:
            return service_type()

        for service in self._services:
            if isinstance(service, service_type):
                return service
        return service_type()

    def has_constraints(self):
        return self._constraints is not None

    def _check_constraints(self, value_to_check):
        if self.has_constraints():
            for v in self._constraints:
                if v.check(value_to_check):
                    continue
                else:
                    type_info = TypeInfos(type(v))
                    self._handle_error_msg(
                        error_type=str(type_info.constraint_type),
                        error_msg=v.error_msg,
                        input_value=value_to_check,
                    )
                    return False
        return True

    def _set_value(self, a_value) -> None:
        if self._value is not None:
            raise AttributeError("value object already set, modification forbidden")
        if self._check_constraints(value_to_check=a_value):
            self._value = a_value

    def _insert_type_constraint(self, contraint: AbstractConstraint):
        contraint_types = [type(c) for c in self._constraints]
        if Required not in contraint_types:
            self._constraints.insert(0, contraint)
        else:
            self._constraints.insert(1, contraint)

    def to_dict(self):
        return self._value
