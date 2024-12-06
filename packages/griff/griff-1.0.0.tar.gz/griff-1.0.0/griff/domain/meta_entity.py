from abc import ABC, ABCMeta
from dataclasses import dataclass
from inspect import get_annotations, signature
from typing import get_args

from griff.domain.auto_vo.base_value_object import BaseValueObject
from griff.domain.auto_vo.generic_factory import (
    GenericAggregateFactoryCompanion,
    GenericEntityFactory,
)
from griff.domain.type_infos import TypeInfos


def factory(cls, services: list = None):
    return GenericEntityFactory(cls._factory_companion, services=services)


@dataclass
class BusinessInvariantDefinition:
    name: str
    method: str


class MetaEntity(ABCMeta, type):
    def get_all_annotations(cls):
        d = {}
        for c in cls.mro():
            if annotations := get_annotations(c, eval_str=True):
                d.update(**annotations)

        return d

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        if ABC in bases:
            return new_cls
        new_cls._fields = cls.get_all_annotations(new_cls)
        new_cls._factory_companion = GenericAggregateFactoryCompanion(
            linked_type=new_cls
        )
        new_cls.factory = classmethod(factory)

        return new_cls

    def _build_field_map(cls):
        from griff.domain.abstract_entity import AbstractEntity

        """
        a field map is a dict, organized like this :
        field_name - str : {
            "type": field_type - type,
            "constraints": - list of AbstractContraints instances -
            "is_entity": is an entity
        }
        """
        field_map = dict()
        if cls._fields is None:
            return {}
        for field_name, field_type in cls._fields.items():
            constraints = None
            is_entity = False
            type_infos = TypeInfos(field_type)
            if type_infos.is_a_list:
                pass
            elif hasattr(field_type, "__metadata__"):
                annotated_args = get_args(field_type)
                field_type = annotated_args[0]
                constraints = {type(e).__name__: e for e in annotated_args[1:]}
                if issubclass(field_type, BaseValueObject):
                    field_type = cls._get_vo_type(field_type)
                elif issubclass(field_type, AbstractEntity):
                    is_entity = True
            elif issubclass(field_type, BaseValueObject):
                field_type = cls._get_vo_type(field_type)
            elif issubclass(field_type, AbstractEntity):
                is_entity = True

            field_map.update(
                {
                    field_name: {
                        "type": field_type,
                        "constraints": constraints,
                        "is_entity": is_entity,
                    }
                }
            )
        return field_map

    def _get_vo_type(cls, vo_type):
        sig = signature(vo_type, eval_str=True)
        if "value" in sig.parameters:
            return sig.parameters["value"].annotation
        return vo_type

    def _is_a_generic_list(cls, a_type):
        return hasattr(a_type, "__origin__") and a_type.__origin__ is list
