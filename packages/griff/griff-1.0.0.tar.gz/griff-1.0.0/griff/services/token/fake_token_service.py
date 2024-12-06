from griff.services.token.token_service import TokenService
from griff.services.uuid.fake_uuid_service import FakeUuidService


class FakeTokenService(FakeUuidService, TokenService):
    def get_token(self) -> str:
        return self.get_uuid()

    def reset(self, last_id=1):
        super().reset(last_id)
