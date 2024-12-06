from griff.domain.auto_vo.base_value_object import AbstractConstraint, BaseValueObject
from griff.domain.type_infos import ConstraintType
from griff.services.uuid.uuid_service import UuidService


class UuidVo(BaseValueObject):
    def __init__(
        self,
        value: str,
        services: list = None,
        constraints: list[AbstractConstraint] = list(),
    ):
        super().__init__(constraints=constraints, services=services)
        self._uuid_service = self._get_service_of_type(UuidService)
        self._error_msg = "is not a valid UUId"
        if value is None:
            value = self._uuid_service.get_uuid()
        try:
            self._uuid_service.validate(value)
        except ValueError:
            self._handle_error_msg(
                error_type=str(ConstraintType.VALUE_INVARIANT),
                error_msg=self._error_msg,
                input_value=value,
            )
            return

        self._set_value(value)
