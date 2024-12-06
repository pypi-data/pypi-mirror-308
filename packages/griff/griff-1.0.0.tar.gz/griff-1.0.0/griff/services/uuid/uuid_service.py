import uuid

from injector import singleton

from griff.services.abstract_service import AbstractService


@singleton
class UuidService(AbstractService):
    def get_uuid(self) -> str:
        return str(uuid.uuid4())

    @staticmethod
    def validate(a_uuid: str):
        uuid.UUID(a_uuid, version=4)
