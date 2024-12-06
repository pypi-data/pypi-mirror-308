from enum import Enum
from inspect import get_annotations
from typing import Any, Mapping

from griff.domain.auto_vo.base_value_object import BaseValueObject
from griff.domain.auto_vo.constraints.required import Required
from griff.domain.type_infos import TypeInfos


class ValueObject(BaseValueObject):
    """
    ValueObject is a base class for all value objects, inherited in declarative way.
    """

    def __init__(
        self,
        value: Mapping[str, Any] = None,
        services: list = None,
        constraints: list = None,
    ):
        super().__init__(
            services=services,
            constraints=constraints,
        )

        if not isinstance(value, Mapping):
            self._set_value(value)
            return

        for attribute, annotation in self._get_annotations().items():
            try:
                field_value = self._check_attribute(
                    value=value.get(attribute),
                    annotation=annotation,
                    field_name=attribute,
                )
            except ValueError:
                field_value = None

            setattr(self, attribute, field_value)

    def _is_required(self, constraints: list) -> bool:
        for c in constraints:
            if isinstance(c, Required):
                return True
        return False

    def _check_attribute(
        self, value: Any, annotation: type, field_name: str = None
    ) -> Any:
        constraints = self._get_constraints(annotation)
        if value is None and not self._is_required(constraints):
            return None
        for constraint in constraints:
            type_info = TypeInfos(type(constraint))
            if not constraint.check(value):
                self._handle_field_error_msg(
                    error_type=str(type_info.constraint_type),
                    field_map=[field_name],
                    error_msg=constraint.error_msg,
                    input_value=value,
                )
                raise ValueError(f"Invalid value for {field_name}: {value}")
        origin = self._get_origin(annotation)
        origin_info = TypeInfos(origin)
        if origin_info.is_a_vo:
            instance = origin(value, services=self._services)
        elif callable(origin):
            instance = origin(value)
        if (
            hasattr(instance, "check_business_invariants")
            and hasattr(instance, "is_valid")
            and instance.is_valid()
        ):
            instance.check_business_invariants()
        return instance

    @classmethod
    def _get_annotations(cls) -> Mapping[str, type]:
        _annotation = get_annotations(cls, eval_str=True)
        for supa_class in cls.__mro__:
            if supa_class == ValueObject:
                break
            _annotation.update(get_annotations(supa_class, eval_str=True))
        return _annotation

    @staticmethod
    def _get_origin(annotation: type) -> type:
        return getattr(annotation, "__origin__", annotation)

    @staticmethod
    def _get_constraints(annotation: type) -> list:
        return getattr(annotation, "__metadata__", ())

    def is_serializable(self, attribute_name, attribute_value: any):
        if attribute_name == "constraints":
            return False

        if attribute_name == "services":
            return False

        if attribute_name == "value":
            return False

        if attribute_name == "field_name":
            return False

        if (
            isinstance(attribute_value, str)
            or isinstance(attribute_value, int)
            or isinstance(attribute_value, list)
            or isinstance(attribute_value, dict)
            or isinstance(attribute_value, Enum)
            or isinstance(attribute_value, BaseValueObject)
            or isinstance(attribute_value, ValueObject)
            or attribute_value is None
        ):
            return True
        return False

    def _is_exlcuded_from_serialization(self, attribute_name, attribute_value):
        if (
            attribute_name == "constraints"
            or attribute_name == "services"
            or attribute_name == "value"
            or attribute_name == "field_name"
        ):
            return True

        if (
            isinstance(attribute_value, str)
            or isinstance(attribute_value, int)
            or isinstance(attribute_value, list)
            or isinstance(attribute_value, dict)
            or isinstance(attribute_value, Enum)
            or isinstance(attribute_value, BaseValueObject)
            or isinstance(attribute_value, ValueObject)
            or attribute_value is None
        ):
            return False
        return True

    def to_dict(self):
        datas = {}
        for attr_name, attr_value in vars(self).items():
            if attr_name.startswith("_"):
                attr_name = attr_name[1:]
            if self._is_exlcuded_from_serialization(
                attribute_name=attr_name, attribute_value=attr_value
            ):
                continue
            if attr_value is None:
                datas.update({attr_name: attr_value})
            elif "to_dict" in dir(attr_value):
                datas.update({attr_name: attr_value.to_dict()})
            else:
                datas.update({attr_name: attr_value})
        return datas

    def _handle_field_error_msg(
        self, error_type: str, field_map: list, error_msg: str, input_value: any
    ):
        self._error_handler.handle_error(error_type, field_map, error_msg, input_value)
