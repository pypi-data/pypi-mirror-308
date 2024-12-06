from injector import inject, singleton

from griff.services.date.fake_date_service import FakeDateService
from griff.services.jwt.jwt_service import JwtService
from griff.services.jwt.jwt_settings import JwtSettings


@singleton
class FakeJwtService(JwtService):
    @inject
    def __init__(self):
        super().__init__(
            JwtSettings(
                access_secret_key="fake-access-secret",
                refresh_secret_key="fake-refresh-secret",
            ),
            FakeDateService(),
        )

    def _create_access_token(self, payload: dict, ts) -> str:
        return "fake-access-token"

    def _create_refresh_token(self, payload: dict, ts) -> str:
        return "fake-refresh-token"
