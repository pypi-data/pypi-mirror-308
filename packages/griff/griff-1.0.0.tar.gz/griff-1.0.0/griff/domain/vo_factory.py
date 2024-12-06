from abc import ABC
from typing import Any

from injector import inject

from griff.domain.abstract_domain_factory import AbstractDomainFactory
from griff.domain.services.constraints_service import ConstraintsService
from griff.domain.type_infos import TypeInfos
from griff.services.date.date_service import DateService
from griff.services.uuid.uuid_service import UuidService


class VoFactory(AbstractDomainFactory, ABC):
    @inject
    def __init__(
        self, uuid_service: UuidService = None, date_service: DateService = None
    ):
        from griff.domain.auto_vo.generic_factory import ListBuilder

        self._list_builder = ListBuilder(self)
        self._uuid_service = uuid_service
        self._date_service = date_service
        self._services = [uuid_service, date_service]

    def hydrate_field(
        self,
        primitive_value,
        field_type: type,
        services: list = None,
        constraints: list = None,
    ) -> Any:
        # hydratation is the same as build_field for value Object
        return self.build_field(  # pragma: no cover
            field_type, primitive_value, services=services, constraints=constraints
        )

    def build_field(
        self,
        field_type: type,
        primitive_value,
        services: list = None,
        constraints: list = None,
    ) -> Any:
        return field_type(primitive_value, constraints=constraints, services=services)

    def build(self, field_type: type, primitive_value, services: list = None):
        type_infos = TypeInfos(field_type)
        priorized_constraints_list = ConstraintsService.prioritize(
            type_infos.constraints
        )

        # check if services needs to overridden
        if services is None:
            services = self._services

        if type_infos.is_a_list:
            return self._list_builder.build_list(
                primitive_value=primitive_value,
                field_type=field_type,
                services=services,
                constraints=priorized_constraints_list,
            )
        else:
            field_instance = self.build_field(
                field_type,
                primitive_value,
                services=services,
                constraints=priorized_constraints_list,
            )
            if field_instance.is_valid() and hasattr(
                field_instance, "check_business_invariants"
            ):
                field_instance.check_business_invariants()
            return field_instance
