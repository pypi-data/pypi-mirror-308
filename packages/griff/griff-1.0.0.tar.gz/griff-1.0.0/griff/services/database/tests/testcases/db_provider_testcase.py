from abc import ABC, abstractmethod
from contextlib import asynccontextmanager

from griff.services.database.database_providers.abstract_db_provider import (
    AbstractDbProvider,
)
from griff.tests_utils.mixins.async_test_mixin import AsyncTestMixin
from griff.tests_utils.mixins.db_test_mixin import DbTestMixin
from griff.tests_utils.testcases.base_testcase import BaseTestCase


# noinspection PyAttributeOutsideInit
class DbProviderTestCase(AsyncTestMixin, DbTestMixin, BaseTestCase, ABC):
    @abstractmethod
    def get_provider(self, settings) -> AbstractDbProvider:
        ...

    @classmethod
    @abstractmethod
    def get_settings(cls):
        ...

    @classmethod
    def init_class_context_data(cls):
        cls.settings = cls.get_settings()
        cls.create_table_sql = (
            "CREATE TABLE lang(id INTEGER PRIMARY KEY, name VARCHAR UNIQUE)"
        )
        cls.drop_table_sql = "DROP TABLE IF EXISTS lang"
        cls.insert_sql = "INSERT INTO lang(id, name) VALUES(1, 'Python')"
        cls.count_sql = "SELECT COUNT(*) as nb FROM lang"
        cls.selectall_sql = "SELECT * FROM lang"

    def init_method_context_data(self):
        self.provider = self.get_provider(self.settings)

    async def async_setup_class(self):
        await super().async_setup_class()
        await self.create_test_db()

    async def async_teardown_class(self):
        await super().async_teardown_class()
        await self.drop_test_db()

    @asynccontextmanager
    async def connect(self):
        await self.provider.start()
        connexion = await self.provider.get_connection()
        try:
            yield connexion
        finally:
            await self.provider.release_connection(connexion)
            await self.provider.stop()

    async def init_db(self, conn):
        await conn.execute(self.drop_table_sql)
        await conn.execute(self.create_table_sql)

    async def insert_data(self, conn):
        await conn.execute(self.insert_sql)

    async def assert_test_table_is_empty(self, conn):
        result = await self.provider.fetch_one(conn, self.count_sql)
        assert result["nb"] == 0

    async def assert_test_table_is_filled(self, conn):
        result = await self.provider.fetch_one(conn, self.selectall_sql)
        assert result == {"id": 1, "name": "Python"}

    """
    execute
    """

    async def test_execute_with_many_request_at_once_return_none(self):
        sql = [self.drop_table_sql, self.create_table_sql, self.insert_sql]
        async with self.connect() as conn:
            await self.provider.execute(conn, sql)
            await self.assert_test_table_is_filled(conn)

    """
    manage connection
    """

    async def test_manage_transaction_with_rollback(self):
        async with self.connect() as connexion:
            await self.init_db(connexion)
            await self.assert_test_table_is_empty(connexion)
            await self.provider.start_transaction(connexion)
            await self.insert_data(connexion)
            await self.provider.rollback_transaction(connexion)
            await self.assert_test_table_is_empty(connexion)

    async def test_manage_transaction_with_commit(self):
        async with self.connect() as connexion:
            await self.init_db(connexion)
            await self.assert_test_table_is_empty(connexion)
            await self.provider.start_transaction(connexion)
            await self.insert_data(connexion)
            await self.provider.commit_transaction(connexion)
            await self.assert_test_table_is_filled(connexion)
