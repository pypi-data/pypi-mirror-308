from injector import singleton

from griff.infrastructure.persistence.repository.persistence_adapter.abstract_persistence_adapter import (  # noqa
    AbstractPersistenceAdapter,
)


@singleton
class MemoryPersistenceAdapter(AbstractPersistenceAdapter):
    def __init__(self):
        self._internal_storage = dict[str, dict]()

    async def persist_new(self, raw_data: dict) -> str:
        return self._persist_new(raw_data)

    async def persist_existing(self, raw_data: dict) -> str:
        if self._internal_storage.get(raw_data["entity_id"], None) is None:
            raise ValueError("Entity not found, impossible to update")

        self._internal_storage[raw_data["entity_id"]] = raw_data
        return raw_data["entity_id"]

    async def remove_from_persistence(self, persistence_id: str) -> None:
        self._internal_storage.pop(persistence_id)

    async def get_from_persistence(self, persistence_id: str) -> dict:
        if self._internal_storage.get(persistence_id, None) is None:
            raise ValueError("Entity not found in persistence, cannot be retrieved")
        return self._internal_storage[persistence_id]

    def reset(self):
        self._internal_storage = dict[str, dict]()

    async def list_with_predicate(self, predicate) -> list[dict]:
        pass  # pragma: no cover

    async def list_all(self) -> list[dict]:
        pass  # pragma: no cover

    async def run_query(self, query_name: str, **query_params):
        method_name = f"{query_name}_query"
        if hasattr(self, method_name):
            return await getattr(self, method_name)(**query_params)
        raise RuntimeError(f"{method_name} not implemented")

    def _get_by_filter(self, filter_name: str, filter_value: str) -> dict:
        for agg in self._internal_storage.values():
            if agg[filter_name] == filter_value:
                return agg
        return None

    def _persist_new(self, raw_data: dict):
        # usefull for test and avoid async setup
        if self._internal_storage.get(raw_data["entity_id"], None) is not None:
            raise ValueError("Entity already exists, cannot be persisted in memory")

        self._internal_storage[raw_data["entity_id"]] = raw_data
        return raw_data["entity_id"]
