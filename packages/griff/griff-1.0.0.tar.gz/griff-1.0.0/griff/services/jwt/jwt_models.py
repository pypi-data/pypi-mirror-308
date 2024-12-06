from dataclasses import dataclass

from griff.mixins.dataclass_mixin import DataclassMixin


@dataclass(frozen=True)
class JwtTokens(DataclassMixin):
    access_token: str
    refresh_token: str


@dataclass(frozen=True)
class DecodedJwtToken(DataclassMixin):
    payload: dict
    has_expired: bool
