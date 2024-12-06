import abc
from contextlib import asynccontextmanager
from typing import List, Union


class AbstractDbProvider(abc.ABC):
    @abc.abstractmethod
    async def start(self):
        pass

    @abc.abstractmethod
    async def stop(self):
        pass

    @abc.abstractmethod
    async def get_connection(self):
        pass

    @abc.abstractmethod
    @asynccontextmanager
    async def transaction(self, connection):
        pass

    @abc.abstractmethod
    async def start_transaction(self, connection):
        pass

    @abc.abstractmethod
    async def commit_transaction(self, connection):
        pass

    @abc.abstractmethod
    async def rollback_transaction(self, connection):
        pass

    @abc.abstractmethod
    async def release_connection(self, connection):
        pass

    @staticmethod
    @abc.abstractmethod
    async def execute(connection, sql: Union[str, List[str]]):
        pass

    @staticmethod
    @abc.abstractmethod
    async def fetch_one(connection, sql) -> dict:
        pass

    @staticmethod
    @abc.abstractmethod
    async def fetch(connection, sql):
        pass

    @abc.abstractmethod
    def get_driver(self) -> str:
        pass

    @abc.abstractmethod
    def get_result_type(self) -> type:
        pass
