from griff.domain.auto_vo.base_value_object import AbstractConstraint, BaseValueObject
from griff.domain.auto_vo.constraints.uuid_constraint import UuidConstraint
from griff.services.uuid.uuid_service import UuidService


class AutoEntityIdVo(BaseValueObject):
    def __init__(
        self,
        value: str = None,
        services: list = None,
        constraints: list[AbstractConstraint] = None,
    ):
        super().__init__(constraints=constraints, services=services)
        self._uuid_service = self._get_service_of_type(UuidService)
        self._error_msg = "is an invalid UUId"
        if value is None and self._has_primary_id_constraint(self._constraints):
            value = self._uuid_service.get_uuid()
        uuid_constraint = UuidConstraint(uuid_service=self._uuid_service)
        self._insert_type_constraint(uuid_constraint)
        self._set_value(value)

    def clone(self):
        return AutoEntityIdVo(
            value=self.value,
            services=self._services,
            constraints=self._constraints,
        )

    def _has_primary_id_constraint(self, constraints_list: list[AbstractConstraint]):
        from griff.domain.auto_vo.constraints.primary_id import PrimaryId

        return PrimaryId in [type(elem) for elem in constraints_list]
