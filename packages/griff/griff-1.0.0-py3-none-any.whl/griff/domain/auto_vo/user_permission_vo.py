from enum import Enum, IntEnum

from griff.domain.auto_vo.base_value_object import BaseValueObject
from griff.domain.auto_vo.constraints.abstract_constraint import AbstractConstraint
from griff.domain.auto_vo.constraints.in_enum import InEnum
from griff.domain.type_infos import TypeInfos


class AbstractUserPermission(IntEnum):
    @classmethod
    def from_str(cls, enum_str):
        for member in cls:
            if member.name == enum_str:
                return member

    def __str__(self):
        return self.name


class UserPermissionType(AbstractUserPermission):
    SUPER_ADMIN = 1
    POWER_USER = 2
    SIMPLE_USER = 3
    GUEST = 1000

    def __str__(self):
        return self.name


class BaseUserPermissionVO(BaseValueObject):
    def __init__(
        self,
        value: list[UserPermissionType | str] = None,
        services: list = None,
        constraints: list[AbstractConstraint] = None,
        linked_permission_enum: Enum = UserPermissionType,
    ):
        super().__init__(services=services, constraints=constraints)
        if value is None and linked_permission_enum is UserPermissionType:
            value = [UserPermissionType.SIMPLE_USER]
        self._linked_enum = linked_permission_enum
        if InEnum not in [type(c) for c in self._constraints]:
            self._insert_type_constraint(InEnum(linked_permission_enum))
        self._set_value(value)

    def _set_value(self, a_value: list) -> None:
        index = 0
        valid = True
        for val in a_value:
            for constr in self._constraints:
                if constr.check(val):
                    continue
                else:
                    valid = False
                    type_info = TypeInfos(type(constr))
                    self._handle_error_msg(
                        error_type=str(type_info.constraint_type),
                        field_map=[index],
                        error_msg=constr.error_msg,
                        input_value=val,
                    )
            index += 1
        if valid:
            if valid:
                self._value = list()
                for val in a_value:
                    if isinstance(val, str):
                        self._value.append(self._linked_enum.from_str(val))
                    elif isinstance(val, self._linked_enum):
                        self._value.append(val)
        else:
            self._value = None

    def has_permission(self, a_permission):
        if isinstance(a_permission, str):
            try:
                a_permission = self._linked_enum.from_str(a_permission)
            except ValueError:
                return False
        if a_permission in self._value:
            return True
        return False

    def get_validation_errors(self, loc="") -> list:
        if loc == "":
            return self._error_handler.get_errors()
        else:
            return self._get_localized_errors(loc)

    def _handle_error_msg(
        self, error_type: str, field_map: list, error_msg: str, input_value: any
    ):
        self._error_handler.handle_error(error_type, field_map, error_msg, input_value)
