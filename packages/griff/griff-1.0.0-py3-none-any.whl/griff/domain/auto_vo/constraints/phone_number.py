from typing import Any

from griff.domain.auto_vo.constraints.abstract_constraint import ValueConstraint
from griff.services.phone_number.phone_number_service import PhoneNumberService


class PhoneNumber(ValueConstraint):
    def __init__(self, phone_number_service: PhoneNumberService = PhoneNumberService()):
        super().__init__()
        self._phone_number_service = phone_number_service
        self._error_msg = "is an invalid phone number"

    def check(self, value: Any) -> bool:
        return self._phone_number_service.is_valid(str(value))
