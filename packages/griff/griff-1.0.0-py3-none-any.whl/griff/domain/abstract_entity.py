from inspect import get_annotations
from typing import Annotated, Set

from griff.domain.auto_vo.auto_entity_id_vo import AutoEntityIdVo
from griff.domain.auto_vo.constraints.primary_id import PrimaryId
from griff.domain.meta_entity import MetaEntity
from griff.domain.serializable import Serializable
from griff.domain.validable import Validable
from griff.domain.with_business_invariant import WithBusinessInvariant
from griff.services.date.date_service import DateService


class AbstractEntity(
    Validable, Serializable, WithBusinessInvariant, metaclass=MetaEntity
):
    _entity_id: Annotated[AutoEntityIdVo, PrimaryId()]

    def __init__(self, **kwargs):
        super().__init__()
        if "entity_id" in kwargs.keys():
            self._entity_id = kwargs.pop("entity_id")
        if "_entity_id" in kwargs.keys():
            self._entity_id = kwargs.pop("_entity_id")

        self._date_service = DateService()
        if "created_at" not in kwargs.keys():
            self._created_at = self._date_service.now()
        if "updated_at" not in kwargs.keys():
            self._updated_at = self._date_service.now()

        member_list = self._get_annotated_attributes()
        for field_name, field_instance in kwargs.items():
            if field_name not in member_list:
                raise ValueError(
                    f"Unknown value object {field_name} for aggregate {type(self)}"
                )
            setattr(self, field_name, field_instance)

        if self.is_valid():
            self.check_business_invariants()

    def __eq__(self, other):
        if not isinstance(other, AbstractEntity):
            return False
        return self.entity_id == other.entity_id

    def is_valid(self) -> bool:
        return len(self.get_validation_errors()) == 0

    def _is_non_empty_list(self, _value):
        return isinstance(_value, list) and len(_value) > 0

    def _get_annotated_attributes(self) -> Set[str]:
        return {
            key for c in type(self).mro() for key in get_annotations(c, eval_str=True)
        }

    def _serialize_list_of_value(self, attr_name, attr_value):
        datas = {}
        if "to_dict" in dir(attr_value[0]):
            datas.update({attr_name: [elem.to_dict() for elem in attr_value]})
        else:
            datas.update({attr_name: attr_value})

        return datas

    def _is_exlcuded_from_serialization(self, attribute_name):
        if (
            attribute_name == "_error_handler"
            or attribute_name == "_events"
            or attribute_name == "_date_service"
            or attribute_name == "_field_name"
            or attribute_name == "_created_at"
            or attribute_name == "_updated_at"
        ):
            return True
        return False

    def to_event(self):
        return self.to_dict()

    def to_history(self):
        return self.to_event()

    def to_dict(self):
        datas = {}
        for attr_name, attr_value in vars(self).items():
            if self._is_exlcuded_from_serialization(attr_name):
                continue
            if attr_name.startswith("_"):
                attr_name = attr_name[1:]

            if "to_dict" in dir(attr_value):
                datas.update({attr_name: attr_value.to_dict()})
            elif self._is_non_empty_list(attr_value):
                datas.update(self._serialize_list_of_value(attr_name, attr_value))
            else:
                datas.update({attr_name: attr_value})
        return datas

    @property
    def entity_id(self):
        return self._entity_id.value

    def __str__(self):
        return f"{self.__class__.__name__}<id={self.entity_id}>"

    @property
    def class_name(self):
        return self.__class__.__name__
