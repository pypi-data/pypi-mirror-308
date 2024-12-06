import inspect
from hashlib import sha256

from injector import singleton

from griff.services.uuid.uuid_service import UuidService


@singleton
class FakeUuidService(UuidService):
    def __init__(self, last_id=1) -> None:
        super().__init__()
        self._start = last_id
        self._referrer_last_uuid = {}

    def get_uuid(self) -> str:
        referrer = self._get_referrer_name()
        if referrer not in self._referrer_last_uuid:
            start_id = self._start + (len(self._referrer_last_uuid.keys()) * 1000)
            self._referrer_last_uuid[referrer] = self._format_id(start_id)

        self._referrer_last_uuid[referrer] = self._increment_id(
            self._referrer_last_uuid[referrer]
        )
        return self._referrer_last_uuid[referrer]

    @staticmethod
    def validate(a_uuid: str):
        if len(a_uuid) != 36:
            raise ValueError("Invalid fake uuid")

    def reset(self, last_id: int = 1):
        self._start = last_id
        self._referrer_last_uuid = {}

    def _increment_id(self, str_id):
        str_id = int(str_id) + 1
        return self._format_id(str_id)

    @staticmethod
    def _format_id(str_id: int) -> str:
        return f"{str_id:036d}"

    def _get_referrer_name(self) -> str:
        entity_name = self._get_entity_name()
        if entity_name is None:
            entity_name = "__unknown__"
        return sha256(entity_name.encode()).hexdigest()

    def _get_entity_name(self):
        for context in inspect.stack():
            if "auto_vo/generic_factory.py" in context.filename:
                try:
                    return str(context[0].f_locals["self"].aggregate_type)
                except Exception:
                    return None
        return None
