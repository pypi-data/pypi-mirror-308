from griff.services.hasher.hasher_service import HasherService
from griff.tests_utils.mixins.stub_mixin import StubMixin


class FakeHasherService(StubMixin, HasherService):
    @staticmethod
    def hash(to_hash: str) -> str:
        # hash for "mon_password"
        return (
            "$pbkdf2-sha256$29000$2hvDOCdkbC1lrJXy3vtf6w$.N5O3fa."
            "y3j7Uhs31YrNwZxbFG3wZP6J9xDQDPnr6Ic"
        )
