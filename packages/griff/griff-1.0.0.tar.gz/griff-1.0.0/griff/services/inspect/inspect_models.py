from enum import Enum
from typing import Any, List

from pydantic import BaseModel, model_validator


class InspectionFieldType(str, Enum):
    str = "str"
    int = "int"
    bool = "bool"
    float = "float"
    list = "list"
    fk = "fk"
    unknown = "unknown"

    @classmethod
    def list_values(cls):
        return list(map(lambda c: c.value, cls))


class InspectionEntityField(BaseModel):
    name: str
    type: InspectionFieldType
    is_required: bool = False
    is_pk: bool = False
    min_length: int = None
    max_length: int = None
    is_entity: bool = False

    @model_validator(mode="before")
    @classmethod
    def validate_and_fullfill_extra_info(cls, data: Any):
        field_type = data["type"]["type"]
        constraints = data["type"]["constraints"]
        prepared_data = {"name": data["name"]}
        if field_type.__name__ in InspectionFieldType.list_values():
            prepared_data["type"] = field_type.__name__
        else:
            prepared_data["type"] = "unknown"

        if data["type"]["is_entity"]:
            prepared_data["is_entity"] = True
            prepared_data["type"] = InspectionFieldType.str
            prepared_data["max_length"] = 36

        if constraints is None:
            return prepared_data
        if "Required" in constraints:
            prepared_data["is_required"] = True
        if "MinLength" in constraints:
            prepared_data["min_length"] = constraints["MinLength"]._min_len
        if "MaxLength" in constraints:
            prepared_data["max_length"] = constraints["MaxLength"]._max_len
        if "PrimaryId" in constraints:
            prepared_data["type"] = InspectionFieldType.str
            prepared_data["is_required"] = True
            prepared_data["max_length"] = 36
            prepared_data["is_pk"] = True
        return prepared_data


class InspectionEntity(BaseModel):
    name: str
    fields: List[InspectionEntityField]
    is_aggregate: bool = False

    @property
    def primary_id(self) -> InspectionEntityField:
        for field in self.fields:
            if field.is_pk:
                return field
        raise RuntimeError("No primary id found")  # pragma: no cover

    @property
    def not_entity_fields(self):
        return [f for f in self.fields if f.is_entity is False]


class InspectionRelation(BaseModel):
    from_entity: str
    from_field: InspectionEntityField
    on_entity: str
    on_field: InspectionEntityField


class InspectionAggregate(BaseModel):
    aggregate: InspectionEntity
    entities: List[InspectionEntity]
    relations: List[InspectionRelation]
