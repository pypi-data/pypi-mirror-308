from typing import Annotated

from griff.domain.abstract_entity import AbstractEntity
from griff.domain.auto_vo.abstract_aggregate_root import AbstractAggregateRoot
from griff.domain.auto_vo.constraints.length import MaxLength, MinLength
from griff.domain.auto_vo.constraints.required import Required
from griff.domain.auto_vo.integer_vo import IntegerVo
from griff.domain.auto_vo.string_vo import StringVo
from griff.domain.value_object import ValueObject


class AggregateWithBaseType(AbstractAggregateRoot):
    _field_str: str
    _field_int: int
    _field_bool: bool
    _field_float: float

    def add_creation_event(self):
        pass


"""
AggregateWithVo
"""

StrListVo = list[StringVo]
RequiredPositiveIntegerVo = Annotated[IntegerVo, Required()]


class AggregateWithVo(AbstractAggregateRoot):
    _name: StringVo
    _required_string: Annotated[StringVo, Required(), MinLength(3), MaxLength(75)]
    _integer: IntegerVo
    _required_integer: RequiredPositiveIntegerVo
    _list_string: StrListVo
    _required_list_string: Annotated[StrListVo, Required()]
    _list_int: list[IntegerVo]
    _required_list_int: Annotated[list[IntegerVo], Required()]

    def add_creation_event(self):
        pass


"""
AggregateWithEntity
"""


class EntityOne(AbstractEntity):
    _name_entity_one: StringVo
    _count: IntegerVo


class EntityTwo(AbstractEntity):
    _name_entity_two: StringVo
    _entity_one: EntityOne


class AggregateWithEntity(AbstractAggregateRoot):
    _name: StringVo
    _integer: RequiredPositiveIntegerVo
    _entity_one: EntityOne
    _entity_two: Annotated[EntityTwo, Required()]
    # list_entities: Annotated[List[EntityOne], Required()]

    def add_creation_event(self):
        pass


"""
AggregateWithOtherAggregate
"""


class AggregateWithOtherAggregate(AbstractAggregateRoot):
    _name: StringVo
    _aggregate_id: AggregateWithEntity

    def add_creation_event(self):
        pass


class ActivityVo(ValueObject):
    ape_code: Annotated[str, Required(), MaxLength(6)]
    name: Annotated[str, Required()]
    details: str

    @property
    def value(self):
        return f"ape_code:{self.ape_code} - {self.name}"

    def to_dict(self):
        return {
            "ape_code": self.ape_code,
            "name": self.name,
            "details": self.details,
        }


class PostalAddressVo(ValueObject):
    line: Annotated[str, Required()]
    zip_code: Annotated[str, Required()]
    city: Annotated[str, Required()]
    country: str
    details: str


class ASimpleValueObject(ValueObject):
    name: Annotated[str, Required()]
    age: int

    @property
    def value(self):
        return f"{self._name} - {self._age}"


class Tags(AbstractEntity):
    tag_name: Annotated[StringVo, Required(), MinLength(3), MaxLength(75)]


class UnderwriterCompany(AbstractAggregateRoot):
    name: Annotated[StringVo, Required(), MinLength(3), MaxLength(75)]
    siret: Annotated[StringVo, MinLength(14), MaxLength(14)]
    ridet: Annotated[StringVo, MinLength(9), MaxLength(10)]
    activity: Annotated[ActivityVo, Required()]
    phone: Annotated[StringVo, Required(), MinLength(8), MaxLength(12)]
    address: Annotated[PostalAddressVo, Required()]
    tag_list: list[Tags]
    dummy_list: list[str]
    simple_list: list[ASimpleValueObject]
    # random_dict: dict[str, str]
