from abc import ABC
from inspect import getmembers
from types import FunctionType
from typing import Any

from griff.domain.type_infos import ConstraintType
from griff.domain.with_error_handler import WithErrorHandler


class WithBusinessInvariant(WithErrorHandler, ABC):
    @classmethod
    def has_business_invariants(cls):
        return len(cls._get_business_invariants()) > 0

    def check_business_invariants(self):
        if not type(self).has_business_invariants():
            return
        for func in type(self)._get_business_invariants():
            invariant_validated = func(self)
            if not invariant_validated:
                if not self._error_already_handled(
                    error_type=str(ConstraintType.BUSINESS_INVARIANT),
                    error_msg=func._business_invariant,
                    input_value="__business_invariant__",
                ):
                    self._handle_error_msg(
                        error_type=str(ConstraintType.BUSINESS_INVARIANT),
                        error_msg=func._business_invariant,
                        input_value="__business_invariant__",
                    )
            if invariant_validated:
                if self._error_already_handled(
                    error_type=str(ConstraintType.BUSINESS_INVARIANT),
                    error_msg=func._business_invariant,
                    input_value="__business_invariant__",
                ):
                    self._drop_error_msg(
                        error_type=str(ConstraintType.BUSINESS_INVARIANT),
                        error_msg=func._business_invariant,
                        input_value="__business_invariant__",
                    )

    @classmethod
    def _get_business_invariants(cls) -> list[FunctionType]:
        def is_business_invariant(member: Any) -> bool:
            return isinstance(member, FunctionType) and hasattr(
                member, "_business_invariant"
            )

        return [value for _, value in getmembers(cls, is_business_invariant)]
