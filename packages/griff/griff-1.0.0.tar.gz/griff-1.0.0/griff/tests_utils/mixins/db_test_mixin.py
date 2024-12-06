import asyncpg
from loguru import logger

from griff.services.database.database_providers.abstract_db_provider import (
    AbstractDbProvider,
)
from griff.services.database.database_providers.asyncpg_provider import AsyncPgProvider
from griff.services.database.db_service import DbService
from griff.services.database.db_test_service import DbTestService


# noinspection SqlResolve
class DbTestMixin:
    provider: AbstractDbProvider = None
    select_all_table = (
        "SELECT table_name FROM information_schema.tables "
        "WHERE table_schema LIKE 'public'"
    )

    @classmethod
    def get_db_service(cls) -> DbService:
        cls.provider = AsyncPgProvider(cls.runtime.get_settings().db)
        return DbTestService(cls.provider)

    @classmethod
    async def drop_all_tables(cls, db_service: DbService):
        await cls._run_on_each_tables(db_service, "drop table __tablename__ CASCADE")

    @classmethod
    async def create_test_db(cls):
        conn = await cls._get_template1_conn()
        try:
            await cls._create_test_db(conn)
        except Exception as e:
            # gestion d'un test qui aurait échoué et qui n'aurait pas fait sont
            # teardown
            logger.error(e)
            await cls._disconnect_all(conn)
            await cls._drop_test_db(conn)
            await cls._create_test_db(conn)
        finally:
            await conn.close()

    @classmethod
    async def _disconnect_all(cls, conn):
        # noinspection SqlInjection
        await cls._get_nb_active_connexion(conn)
        sql = (
            "SELECT pg_terminate_backend(pg_stat_activity.pid) "
            "FROM pg_stat_activity "
            f"WHERE pg_stat_activity.datname = '{cls.runtime.get_settings().db.name}' "
            "AND pid <> pg_backend_pid();"
        )
        await conn.execute(sql)

    @classmethod
    async def get_nb_active_connexion(cls):
        conn = await cls._get_template1_conn()
        try:
            return await cls._get_nb_active_connexion(conn)
        finally:
            await conn.close()

    @classmethod
    async def _get_nb_active_connexion(cls, conn):
        row = await conn.fetchrow(
            "SELECT sum(numbackends) as nb FROM pg_stat_database;"
        )
        print(f"{row['nb']} connexion active")
        return row["nb"]

    @classmethod
    async def drop_test_db(cls):
        conn = await cls._get_template1_conn()
        try:
            await cls._drop_test_db(conn)
        except Exception as e:
            print(f"ERROR: {e}")
        finally:
            await conn.close()

    @classmethod
    async def _run_on_each_tables(cls, db_service: DbService, base_sql: str):
        async with db_service.get_connection() as connection:
            rows = await db_service._provider.fetch(connection, cls.select_all_table)
            sql = []
            for row in rows:
                sql.append(f"{base_sql.replace('__tablename__', row['table_name'])}")
            if sql:
                await db_service._provider.execute(connection, sql)

    @classmethod
    async def _get_template1_conn(cls):
        settings = cls.runtime.get_settings().db.copy(deep=True)
        settings.name = "template1"
        return await asyncpg.connect(settings.connection_string)

    @classmethod
    async def _create_test_db(cls, conn):
        # noinspection SqlInjection
        sql = f"CREATE DATABASE {cls.runtime.get_settings().db.name}"
        await conn.execute(sql)

    @classmethod
    async def _drop_test_db(cls, conn):
        # noinspection SqlInjection
        sql = f"DROP DATABASE {cls.runtime.get_settings().db.name}"
        await conn.execute(sql)
