from contextlib import asynccontextmanager

from griff.services.database.database_providers.abstract_db_provider import (
    AbstractDbProvider,
)


class FakeDbProvider(AbstractDbProvider):
    def __init__(self) -> None:
        super().__init__()
        self.transaction_started = 0
        self.transaction_commit = 0
        self.transaction_rollback = 0
        self.connection_started = 0
        self.connection_release = 0

    def get_driver(self) -> str:
        return "fake-db"

    async def start(self):
        pass

    async def stop(self):
        pass

    @asynccontextmanager
    async def transaction(self, connection):
        self.transaction_started += 1
        try:
            yield connection
            self.transaction_commit += 1
        except Exception as e:
            self.transaction_rollback += 1
            raise e

    async def get_connection(self):
        self.connection_started += 1
        return "fake-connexion"

    def get_result_type(self) -> type:
        return dict

    async def start_transaction(self, connection):
        self.transaction_started += 1

    async def commit_transaction(self, connection):
        self.transaction_commit += 1

    async def rollback_transaction(self, connection):
        self.transaction_rollback += 1

    async def release_connection(self, connection):
        self.connection_release += 1

    def release_pool(self):
        pass

    @staticmethod
    async def execute(connection, sql):
        pass

    @staticmethod
    async def fetch_one(connection, sql) -> dict:
        return {"fake": "data"}

    @staticmethod
    async def fetch(connection, sql):
        return [{"fake": "data"}, {"fake": "data"}]
