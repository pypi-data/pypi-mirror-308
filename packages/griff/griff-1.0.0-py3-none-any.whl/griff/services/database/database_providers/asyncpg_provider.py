import threading
from contextlib import asynccontextmanager
from typing import List, Union

import asyncpg
from asyncpg import Record
from injector import inject, singleton
from loguru import logger

from griff.services.database.database_providers.abstract_db_provider import (
    AbstractDbProvider,
)
from griff.services.database.db_settings import DbSettings


@singleton
class AsyncPgProvider(AbstractDbProvider):
    @inject
    def __init__(self, settings: DbSettings):
        self.connection_dsn = settings.connection_string
        self._async_connection_pool = None
        self._transactions = {}
        self._debug = False

    async def start(self):
        if self._async_connection_pool is None:
            self.debug("--->STARTING POOL")
            self._async_connection_pool = await asyncpg.create_pool(
                dsn=self.connection_dsn, min_size=10, max_size=50
            )

    async def stop(self):
        if self._async_connection_pool is None:
            return None
        self.debug("--->CLOSING POOL")
        self._async_connection_pool.terminate()
        self._async_connection_pool = None

    async def get_connection(self):
        self.debug(f"Getting connection from provider: ---------------  {id(self)} ")
        connection = await self._async_connection_pool.acquire()
        self.debug(
            f"connection {self.get_conn_id(connection)} acquired from pool "
            f"{id(self._async_connection_pool)}"
        )
        self.debug(f"---- {self._async_connection_pool.get_idle_size()} - left in pool")
        return connection

    @asynccontextmanager
    async def transaction(self, connection):
        conn_id = self.get_conn_id(connection)

        async with connection.transaction():
            self.debug(f"Start transaction --- on connection {conn_id}")
            yield
            self.debug(f"End transaction --- on connection {conn_id}")

    async def start_transaction(self, connection):
        conn_id = id(connection)
        self._transactions[conn_id] = connection.transaction()
        self.debug(f"starting transaction on connection {conn_id}")
        await self._transactions[conn_id].start()
        self.debug(f"started transaction  on connection {conn_id}")

    async def rollback_transaction(self, connection):
        # check we're working on the right connection
        if self._transactions[id(connection)]._connection == connection._con:
            await self._transactions[id(connection)].rollback()
            self._transactions[id(connection)] = None
        else:
            raise Exception("Transaction not found")

    async def commit_transaction(self, connection):
        conn_id = id(connection)
        await self._transactions[conn_id].commit()
        self.debug(f"commit transaction--- on connection {conn_id} ")
        self._transactions.pop(conn_id)

    async def release_connection(self, connection):
        conn_id = id(connection)
        self.debug(f"releasing connection --- on connection {conn_id}")
        try:
            await self._async_connection_pool.release(connection)
        except Exception as e:
            self.debug(f"Error releasing connection: {e}")
            raise e
        self.debug(f"released connection --- on connection {conn_id}")

    def get_driver(self) -> str:
        return "asyncpg"

    def get_result_type(self) -> type:
        return Record

    def debug(self, msg):  # pragma: no cover
        if self._debug is True:
            logger.debug(
                f"  PROVIDER --  thread ID : {threading.current_thread().ident} {msg}"
            )

    @staticmethod
    async def execute(connection, sql: Union[str, List[str]]):
        if isinstance(sql, list):
            sql = ";\n".join(sql)
        await connection.execute(sql)

    async def fetch_one(self, connection, sql) -> dict:
        # return await self.fetch(connection, sql)
        row = await connection.fetchrow(sql)
        return dict(row)

    @staticmethod
    async def fetch(connection, sql):
        rows = await connection.fetch(sql)
        return [dict(row) for row in rows]

    @staticmethod
    def get_conn_id(connection):
        return id(connection)
