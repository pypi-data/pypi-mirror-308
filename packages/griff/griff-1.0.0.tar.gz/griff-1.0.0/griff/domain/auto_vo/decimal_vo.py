from decimal import Decimal, InvalidOperation

from griff.domain.auto_vo.base_value_object import AbstractConstraint, BaseValueObject
from griff.domain.type_infos import ConstraintType


class DecimalVo(BaseValueObject):
    def __init__(
        self,
        value: Decimal | str | int | float,
        services: list = None,
        constraints: list[AbstractConstraint] = list(),
    ):
        super().__init__(services=services, constraints=constraints)
        try:
            dec_value = Decimal(value)
        except InvalidOperation:
            self._handle_error_msg(
                error_type=str(ConstraintType.STRUCTURAL_INVARIANT),
                error_msg="is not a valid decimal",
                input_value=value,
            )
            return
        self._set_value(dec_value)

    def _set_value(self, a_value) -> None:
        if self._value is not None:
            raise AttributeError("value object already set, modification forbidden")
        if self._check_constraints(value_to_check=a_value):
            self._value = Decimal(a_value)
