from injector import singleton
from passlib.handlers.pbkdf2 import pbkdf2_sha256

from griff.services.abstract_service import AbstractService


@singleton
class HasherService(AbstractService):
    @staticmethod
    def hash(to_hash: str) -> str:
        return pbkdf2_sha256.hash(to_hash)

    @staticmethod
    def verify(candidate: str, reference: str):
        return pbkdf2_sha256.verify(candidate, reference)
