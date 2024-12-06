import phonenumbers
from injector import singleton

from griff.services.abstract_service import AbstractService


@singleton
class PhoneNumberService(AbstractService):
    def __init__(self, default_region: str = "FR"):
        self._default_region = default_region

    def is_valid(self, phone_number: str, region: str = None) -> bool:
        try:
            number = phonenumbers.parse(
                phone_number,
                region or self._default_region,
            )
        except phonenumbers.NumberParseException:
            return False

        return phonenumbers.is_valid_number(number)
