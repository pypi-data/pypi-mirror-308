from injector import singleton

from griff.services.uuid.uuid_service import UuidService


@singleton
class TokenService(UuidService):
    def get_token(self) -> str:
        return self.get_uuid()
