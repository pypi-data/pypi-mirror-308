from griff.domain.auto_vo.constraints.abstract_constraint import ValueConstraint
from griff.services.uuid.uuid_service import UuidService


class UuidConstraint(ValueConstraint):
    def __init__(self, uuid_service: UuidService = UuidService()):
        super().__init__()
        self._uuid_service = uuid_service
        self._error_msg = "is an invalid UUId"

    def check(self, value):
        try:
            self._uuid_service.validate(value)
            return True
        except ValueError:
            return False
