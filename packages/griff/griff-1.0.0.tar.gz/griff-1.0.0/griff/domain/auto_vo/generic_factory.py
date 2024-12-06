import inspect
from abc import ABC
from typing import Any

from griff.domain.abstract_domain_factory import AbstractDomainFactory
from griff.domain.auto_vo.constraints.abstract_constraint import AbstractConstraint
from griff.domain.auto_vo.constraints.base_constraint.list import ListConstraint
from griff.domain.auto_vo.constraints.in_enum import InEnum
from griff.domain.auto_vo.constraints.primary_id import PrimaryId
from griff.domain.auto_vo.constraints.required import Required
from griff.domain.auto_vo.enum_vo import EnumVo
from griff.domain.list_wrapper import ListWrapper
from griff.domain.services.constraints_service import ConstraintsService
from griff.domain.type_infos import ListNature, TypeInfos
from griff.domain.vo_factory import VoFactory


class GenericAggregateFactoryCompanion(ABC):
    def __init__(self, linked_type: type):
        self._linked_type = linked_type

    @property
    def target_type(self):
        return self._linked_type

    @property
    def fields(self):
        if hasattr(self._linked_type, "_fields"):
            return self._linked_type._fields
        return {}


class ListBuilder(ABC):
    def __init__(self, linked_factory: AbstractDomainFactory):
        self._linked_factory = linked_factory

    def _check_list_constraints(
        self, primitive_value, constraints, wrapped_list: ListWrapper
    ) -> bool:
        constraints.insert(1, ListConstraint())
        for constraint in constraints:
            if not constraint.check(primitive_value):
                wrapped_list.add_list_level_error(
                    input_value=primitive_value, error_msg=constraint.error_msg
                )
                if isinstance(constraint, Required):
                    return wrapped_list
                else:
                    break

    def _process_list(
        self,
        primitive_value,
        field_type,
        services,
        constraints,
        wrapped_list: ListWrapper = None,
        element_builder=None,
        list_builder=None,
    ):
        if wrapped_list is None:
            wrapped_list = ListWrapper()
        type_infos = TypeInfos(field_type)
        if (
            type_infos.list_nature == ListNature.ANNOTATED_UNTYPED
            or type_infos.list_nature == ListNature.ANNOTATED_TYPED
        ):
            # - if list is annotated, we have to checks constraints, before building it # noqa
            self._check_list_constraints(
                primitive_value=primitive_value,
                constraints=constraints,
                wrapped_list=wrapped_list,
            )

        if type_infos.list_nature == ListNature.ANNOTATED_TYPED:
            # - if list is an annotated list, decrease one level of annotation
            vo_list = list_builder(
                primitive_value=primitive_value,
                field_type=type_infos.inner_type_infos.typ,
                services=services,
                constraints=type_infos.inner_type_infos.constraints,
                wrapped_list=wrapped_list,
            )
            return vo_list
        if type_infos.list_nature == ListNature.BASIC_TYPED:
            # - if list is a basic typed list, just build each element of the list,
            # if primitive_value is not None
            index_of_element = 0
            if primitive_value is None:
                return wrapped_list
            for elem in primitive_value:
                if type_infos.inner_type_infos.is_an_enum:
                    enum_constraint = InEnum(type_infos.inner_type_infos.typ)
                    enum_vo = EnumVo(
                        value=elem,
                        services=services,
                        constraints=[enum_constraint],
                    )
                    wrapped_list.append(enum_vo)
                elif (
                    type_infos.inner_type_infos.is_a_vo
                    or type_infos.inner_type_infos.is_an_entity
                    or type_infos.inner_type_infos.is_a_list
                ):
                    vo_element = element_builder(
                        primitive_value=elem,
                        field_type=type_infos.inner_type_infos.typ,
                        services=services,
                        constraints=type_infos.inner_type_infos.constraints,
                    )
                    wrapped_list.append(vo_element)
                else:
                    vo_element = type_infos.inner_type_infos.typ(elem)
                    wrapped_list.append(vo_element)
                index_of_element += 1
            return wrapped_list

        if (
            type_infos.list_nature == ListNature.ANNOTATED_UNTYPED
            or type_infos.list_nature == ListNature.BASIC_UNTYPED
        ):
            # if list is untyped, just retrieve the primitive value
            wrapped_list.set_inner_list(primitive_value)
            return wrapped_list

    def hydrate_list(
        self,
        primitive_value,
        field_type,
        services,
        constraints,
        wrapped_list: ListWrapper = None,
    ):
        return self._process_list(
            primitive_value=primitive_value,
            field_type=field_type,
            services=services,
            constraints=constraints,
            wrapped_list=wrapped_list,
            element_builder=self._linked_factory.hydrate_field,
            list_builder=self.hydrate_list,
        )

    def build_list(
        self,
        primitive_value,
        field_type,
        services,
        constraints,
        wrapped_list: ListWrapper = None,
    ) -> ListWrapper:
        return self._process_list(
            primitive_value=primitive_value,
            field_type=field_type,
            services=services,
            constraints=constraints,
            wrapped_list=wrapped_list,
            element_builder=self._linked_factory.build_field,
            list_builder=self.build_list,
        )


class GenericEntityFactory(AbstractDomainFactory, ABC):
    def __init__(self, _companion: GenericAggregateFactoryCompanion, services: list):
        self._service_map = dict()
        self._service_list = services
        if _companion is not None:
            self._field_map = self._build_field_map(_companion.fields)
            self._linked_type = _companion.target_type
            self._aggregate_fields = (
                _companion.fields
            )  # TBD: Refacto pour passer uniquement au field map
        self._list_builder = ListBuilder(self)
        self._vo_factory = VoFactory()

    def _build_field_map(self, field_dict):
        """
        a field map is a dict, organized like this :
        field_name - str : { "type": field_type - type,
                       "constraints": - list of AbstractContraints instances -
        """
        field_map = dict()
        if field_dict is None or len(field_dict) == 0:
            return {}

        self.assert_primary_constraint_is_set(field_dict)

        for field_name, field_type in field_dict.items():
            dynamic_constraints = None
            if hasattr(field_type, "__metadata__"):
                dynamic_constraints = list(field_type.__metadata__)

            ordered_constraints = ConstraintsService.prioritize(dynamic_constraints)
            field_map.update(
                {field_name: {"type": field_type, "constraints": ordered_constraints}}
            )
        return field_map

    def _is_primary_ID(self, constraints_list: list[AbstractConstraint]):
        return PrimaryId in [type(elem) for elem in constraints_list]

    def _is_field_required(self, constraints_list: list[AbstractConstraint]):
        return not constraints_list[0].check(None)

    def assert_primary_constraint_is_set(self, field_list: dict):
        constraints = list()
        for field_type in [
            ft for ft in field_list.values() if hasattr(ft, "__metadata__")
        ]:
            constraints.extend(list(field_type.__metadata__))
        if PrimaryId not in [type(elem) for elem in constraints]:
            raise RuntimeError(f"PrimaryId shall be defined on {self._linked_type}")

    def _has_a_method(self, method_name, an_instance):
        return method_name in dir(an_instance)

    def hydrate_field(
        self,
        primitive_value,
        field_type: type,
        services: list = None,
        constraints: list = None,
    ) -> Any:
        if primitive_value is None and not self._is_field_required(constraints):
            return None

        type_infos = TypeInfos(field_type)

        if type_infos.is_a_list:
            return self._list_builder.hydrate_list(
                primitive_value=primitive_value,
                field_type=field_type,
                services=services,
                constraints=constraints,
            )

        elif type_infos.is_an_entity:
            if primitive_value is None:
                primitive_value = {}
            return field_type.factory(services=self._service_list).hydrate(
                primitive_value
            )
        elif type_infos.is_a_vo:
            return self._vo_factory.build(
                field_type=field_type,
                primitive_value=primitive_value,
                services=services,
            )
        else:
            return field_type(primitive_value)

    def build_field(
        self,
        field_type: type,
        primitive_value,
        services: list = None,
        constraints: list = None,
    ) -> Any:
        if primitive_value is None and not self._is_field_required(constraints):
            return None

        type_infos = TypeInfos(field_type)

        if type_infos.is_a_list:
            return self._list_builder.build_list(
                primitive_value=primitive_value,
                field_type=field_type,
                services=services,
                constraints=constraints,
            )
        elif type_infos.is_an_entity:
            if primitive_value is None:
                primitive_value = {}
            return field_type.factory(services=self._service_list).build(
                **primitive_value
            )
        elif type_infos.is_a_vo:
            return self._vo_factory.build(
                field_type=field_type,
                primitive_value=primitive_value,
                services=services,
            )
        else:
            return field_type(primitive_value)

    def patch(self, instance_to_patch, **kwargs):
        vo_pool = dict()
        sanitized_args = kwargs

        for field_name, field_type in self._aggregate_fields.items():
            type_infos = TypeInfos(field_type)
            primitive_value = sanitized_args.get(field_name, None)
            if primitive_value is None:
                primitive_value = sanitized_args.get(f"{field_name[1:]}", None)

            if primitive_value is None and field_name not in kwargs.keys():
                continue

            dynamic_constraints = type_infos.constraints
            ordered_constraints = ConstraintsService.prioritize(dynamic_constraints)

            # if field is primary_id, try to build it, anyway
            if self._is_primary_ID(ordered_constraints):
                raise RuntimeError("entity id shall not be set at patch time")

            built = self.build_field(
                primitive_value=primitive_value,
                field_type=field_type,
                services=self._service_list,
                constraints=ordered_constraints,
            )
            if built is None and hasattr(self._linked_type, field_name):
                value = getattr(self._linked_type, field_name)
                if not inspect.isroutine(value) and not inspect.isclass(value):
                    vo_pool[f"{field_name}"] = value
            else:
                vo_pool[f"{field_name}"] = built

        # replace all fields in instance_to_patch
        for field_name, field_value in vo_pool.items():
            setattr(instance_to_patch, field_name, field_value)

        instance_to_patch.check_business_invariants()

        return instance_to_patch

    def build(self, **kwargs):
        vo_pool = dict()
        sanitized_args = kwargs

        self.assert_primary_constraint_is_set(self._aggregate_fields)

        for field_name, field_type in self._aggregate_fields.items():
            type_infos = TypeInfos(field_type)
            primitive_value = sanitized_args.get(field_name, None)
            if primitive_value is None:
                primitive_value = sanitized_args.get(f"{field_name[1:]}", None)
            dynamic_constraints = type_infos.constraints
            ordered_constraints = ConstraintsService.prioritize(dynamic_constraints)

            # if field is primary_id, try to build it, anyway
            if self._is_primary_ID(ordered_constraints):
                if primitive_value is not None:
                    raise RuntimeError(
                        "Primary Entity_id shall not be set at build time, "
                        "use Hydrate method to get an existing aggregate, "
                        "or remove PrimaryId if referencing an external aggregate"
                    )
                vo_pool[f"{field_name}"] = field_type(
                    value=primitive_value,
                    services=self._service_list,
                    constraints=ordered_constraints,
                )
                # continue to loop on fields after having build primary_id
                continue

            built = self.build_field(
                primitive_value=primitive_value,
                field_type=field_type,
                services=self._service_list,
                constraints=ordered_constraints,
            )
            if built is None and hasattr(self._linked_type, field_name):
                value = getattr(self._linked_type, field_name)
                if not inspect.isroutine(value) and not inspect.isclass(value):
                    vo_pool[f"{field_name}"] = value
            else:
                vo_pool[f"{field_name}"] = built

        new_aggregate = self._linked_type(**vo_pool)

        if (
            self._has_a_method("add_creation_event", new_aggregate)
            and new_aggregate.is_valid()
        ):
            new_aggregate.add_creation_event()

        return new_aggregate

    def hydrate(self, agg_as_dict: dict):
        # try to match aggregate field, with dict datas
        vo_pool = {}
        for field_name, field_data in self._field_map.items():
            field_value = agg_as_dict.get(field_name, None)
            if field_value is None:
                field_value = agg_as_dict.get(f"{field_name[1:]}", None)

            field_type = field_data.get("type", None)
            if field_type is None:
                raise RuntimeError(
                    f"{field_value} type is unknown, impossible to hydrate aggregate"
                )
            field_constraints = field_data.get("constraints", None)

            if field_constraints is None:
                raise RuntimeError(
                    f"{field_value} constraints are unknown, "
                    f"impossible to hydrate aggregate"
                )

            if self._is_primary_ID(field_constraints):
                if field_value is None:
                    raise RuntimeError(
                        "entity_id None is forbidden !!"
                        "impossible to hydrate aggregate"
                    )

            vo_pool[f"{field_name}"] = self.hydrate_field(
                primitive_value=field_value,
                field_type=field_type,
                services=self._service_list,
                constraints=field_constraints,
            )

        new_aggregate = self._linked_type(**vo_pool)
        return new_aggregate

    @property
    def aggregate_type(self) -> type:
        return self._linked_type
