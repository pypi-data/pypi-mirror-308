from enum import Enum
from types import GenericAlias

from griff.domain.auto_vo.constraints.abstract_constraint import (
    BusinessConstraint,
    ValueConstraint,
)


class ListNature(Enum):
    # when field is just a list like, toto: list
    BASIC_UNTYPED = "BASIC"
    # when field is typed list like, toto: list[str]
    BASIC_TYPED = "TYPED"
    # when field is annotated list like, toto: Annotated[list, Required()]
    ANNOTATED_UNTYPED = "ANNOTATED"
    # when field is annotated list like, toto: Annotated[list[str], Required()]
    ANNOTATED_TYPED = "ANNOTATED_TYPED"


class ConstraintType(Enum):
    BUSINESS_INVARIANT = "business_invariant"
    STRUCTURAL_INVARIANT = "structural_invariant"
    VALUE_INVARIANT = "value_invariant"

    def __str__(self):
        return self.value


class TypeInfos:
    def __init__(self, a_type):
        self._type = a_type
        self._is_list = self._is_a_list(a_type)
        if self.inner_type is not None:
            self._inner_type_infos = TypeInfos(self.inner_type)
        else:
            self._inner_type_infos = None

    @property
    def inner_type_infos(self):
        return self._inner_type_infos

    @property
    def is_annotated(self):
        return hasattr(self._type, "__metadata__")

    @property
    def constraints(self):
        if self.is_annotated:
            return list(self._type.__metadata__)
        return None

    @property
    def inner_type(self):
        if self.is_annotated:
            return self._type.__origin__
        if self._is_a_list(self._type):
            return self._get_internal_list_type(self._type)
        return None

    @property
    def is_a_list(self):
        return self._is_list

    @property
    def list_nature(self):
        if not self.is_a_list:
            return None
        return self._get_list_nature(self._type)

    def _is_a_list(self, a_type) -> bool:
        if hasattr(a_type, "__origin__"):
            return self._is_a_list(a_type.__origin__)
        return self._is_a_basic_list(a_type)

    def _is_a_basic_list(self, a_type) -> bool:
        return (
            a_type is type
            and issubclass(a_type, list)
            or a_type is list
            or isinstance(a_type, GenericAlias)
        )

    def _get_internal_list_type(self, a_list_type):
        a_list_nature = self._get_list_nature(a_list_type)
        if a_list_nature == ListNature.BASIC_UNTYPED:
            return None

        if a_list_nature == ListNature.ANNOTATED_UNTYPED:
            return None

        if a_list_nature == ListNature.BASIC_TYPED:
            return a_list_type.__args__[0]

        if a_list_nature == ListNature.ANNOTATED_TYPED:
            return self._get_internal_list_type(a_list_type.__origin__)

    def _get_list_nature(self, a_list_type):
        if self._is_a_basic_list(a_list_type):
            if self._is_inner_type_typed(a_list_type):
                return ListNature.BASIC_TYPED
            return ListNature.BASIC_UNTYPED
        else:
            if hasattr(a_list_type, "__origin__"):
                if (
                    self._get_list_nature(a_list_type.__origin__)
                    == ListNature.BASIC_TYPED
                ):
                    return ListNature.ANNOTATED_TYPED
                else:
                    return ListNature.ANNOTATED_UNTYPED

    def _is_inner_type_typed(self, a_type) -> bool:
        if hasattr(a_type, "__args__") and len(a_type.__args__) > 0:
            return True
        else:
            return False

    @property
    def typ(self):
        return self._type

    @property
    def is_a_vo_or_entity(self):
        from griff.domain.abstract_entity import AbstractEntity
        from griff.domain.auto_vo.base_value_object import BaseValueObject
        from griff.domain.value_object import ValueObject

        if self.is_a_list:
            return False

        if self.is_annotated:
            return False

        return (
            issubclass(self._type, BaseValueObject)
            or issubclass(self._type, ValueObject)
            or issubclass(self._type, AbstractEntity)
        )

    @property
    def is_an_entity(self):
        from griff.domain.abstract_entity import AbstractEntity

        if self.is_annotated:
            return self._inner_type_infos.is_an_entity

        if self.is_a_list:
            return False

        return issubclass(self._type, AbstractEntity)

    @property
    def is_a_vo(self):
        import inspect

        from griff.domain.auto_vo.base_value_object import BaseValueObject
        from griff.domain.value_object import ValueObject

        if self.is_a_list:
            return False

        if self.is_annotated:
            return self._inner_type_infos.is_a_vo

        return inspect.isclass(self._type) and (
            issubclass(self._type, BaseValueObject)
            or issubclass(self._type, ValueObject)
        )

    @property
    def is_a_base_vo(self):
        from griff.domain.auto_vo.base_value_object import BaseValueObject

        if self.is_a_list:
            return False

        if self.is_annotated:
            return self._inner_type_infos.is_a_base_vo

        return issubclass(self._type, BaseValueObject)

    @property
    def is_a_compound_vo(self):
        from griff.domain.value_object import ValueObject

        if self.is_a_list:
            return False

        if self.is_annotated:
            return self._inner_type_infos.is_a_compound_vo

        return issubclass(self._type, ValueObject)

    @property
    def is_a_basic_type(self):
        return (
            self._type == str
            or self._type == int
            or self._type == float
            or self._type == bool
        )

    @property
    def is_a_list_wrapper(self):
        from griff.domain.list_wrapper import ListWrapper

        return issubclass(self._type, ListWrapper)

    @property
    def is_a_constraint(self):
        from griff.domain.auto_vo.constraints.abstract_constraint import (
            AbstractConstraint,
        )

        if self.is_annotated:
            return False
        return issubclass(self._type, AbstractConstraint)

    @property
    def constraint_type(self):
        from griff.domain.auto_vo.constraints.abstract_constraint import (
            StructureConstraint,
        )

        if issubclass(self._type, StructureConstraint):
            return ConstraintType.STRUCTURAL_INVARIANT
        if issubclass(self._type, BusinessConstraint):
            return ConstraintType.BUSINESS_INVARIANT
        if issubclass(self._type, ValueConstraint):
            return ConstraintType.VALUE_INVARIANT

    @property
    def is_an_enum(self):
        if self.is_annotated:
            return False
        return issubclass(self._type, Enum)

    @property
    def has_constraints(self):
        return self.constraints is not None

    @property
    def is_an_enum_vo(self):
        from griff.domain.auto_vo.enum_vo import EnumVo

        if self.is_annotated:
            return False
        return issubclass(self._type, EnumVo)
