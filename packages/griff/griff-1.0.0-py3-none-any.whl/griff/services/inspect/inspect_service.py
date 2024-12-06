from typing import Type

from griff.domain.abstract_entity import AbstractEntity
from griff.domain.auto_vo.abstract_aggregate_root import AbstractAggregateRoot
from griff.services.abstract_service import AbstractService
from griff.services.inspect.inspect_models import (
    InspectionAggregate,
    InspectionEntity,
    InspectionEntityField,
    InspectionRelation,
)


class InspectService(AbstractService):
    def inspect_aggregate(
        self, klass: Type[AbstractAggregateRoot]
    ) -> InspectionAggregate:
        entities = {}
        relations = []
        inspected = self._inspect_entity(klass, entities, relations)
        return InspectionAggregate(
            aggregate=inspected,
            entities=list(entities.values()),
            relations=relations,
        )

    def _inspect_entity(
        self, klass: Type[AbstractEntity], entities: dict, relations: list
    ):
        field_map = klass._build_field_map()
        fields = {}
        for n, t in field_map.items():
            fields[n] = InspectionEntityField(name=n, type=t)
            if t["is_entity"] is True:
                entity_name = self._get_entity_name(t["type"])
                if entity_name not in entities:
                    entities[entity_name] = self._inspect_entity(
                        t["type"], entities, relations
                    )
                relations.append(
                    InspectionRelation(
                        from_entity=self._get_entity_name(klass),
                        from_field=fields[n],
                        on_entity=entities[entity_name].name,
                        on_field=entities[entity_name].primary_id,
                    )
                )

        if "_entity_id" in fields:
            # set entity_id at first place
            fields = {"_entity_id": fields.pop("_entity_id"), **fields}
        return InspectionEntity(
            name=self._get_entity_name(klass),
            fields=fields.values(),
            is_aggregate=AbstractAggregateRoot in klass.__mro__,
        )

    @staticmethod
    def _get_entity_name(klass: Type[AbstractEntity]):
        return klass.__name__.lower()
