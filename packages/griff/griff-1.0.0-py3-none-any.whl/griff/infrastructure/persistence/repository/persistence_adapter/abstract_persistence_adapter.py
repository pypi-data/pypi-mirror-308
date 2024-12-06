from abc import ABC, abstractmethod


class AbstractPersistenceAdapter(ABC):
    @abstractmethod
    async def persist_new(self, raw_data: dict) -> str:
        """
        shall raise RuntimeError if anything goes wrong
        """
        pass  # pragma: no cover

    @abstractmethod
    async def persist_existing(self, raw_data: dict) -> str:
        pass  # pragma: no cover

    @abstractmethod
    async def remove_from_persistence(self, persistence_id: str) -> None:
        pass  # pragma: no cover

    @abstractmethod
    async def get_from_persistence(self, persistence_id: str) -> dict:
        pass  # pragma: no cover

    @abstractmethod
    async def list_with_predicate(self, predicate) -> list[dict]:
        pass  # pragma: no cover

    @abstractmethod
    async def list_all(self) -> list[dict]:
        pass  # pragma: no cover

    @abstractmethod
    async def run_query(self, query_name: str, **query_params):
        pass
