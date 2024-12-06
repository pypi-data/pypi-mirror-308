from importlib.machinery import SourceFileLoader
from pathlib import Path

import asyncpg

from griff.settings.griff_settings import GriffSettings
from griff.utils.migration_utils import MigrationUtils


# noinspection SqlInjection
class DbTplUtils:
    def __init__(self, context: str, settings: GriffSettings):
        self.context = context
        self.settings = settings
        self.default_db_name = self.settings.db.name
        self.tpl_db_name = f"test_{self.settings.project}_{self.context}"

    @property
    def persistence_path(self) -> Path:
        return self.settings.get_persistence_path(self.context)

    @property
    def db_tpl_path(self) -> Path:
        return self.persistence_path.joinpath("_db_tpl")

    @property
    def dump_filename(self) -> Path:
        return self.db_tpl_path.joinpath("db_tpl.dump")

    @property
    def dump_sql_filename(self) -> Path:
        return self.db_tpl_path.joinpath("db_tpl.sql")

    def is_context_exists(self):
        context_path = self.settings.get_context_path(self.context)
        return context_path.exists()

    def has_initial_data(self):
        return self._initial_data_path.exists()

    async def create(self):
        conn = await self._get_template1_conn()
        try:
            await self._create(conn)
        finally:
            await conn.close()

    async def is_db_exists(self):
        settings = self.settings.db.model_copy(deep=True)
        settings.name = self.tpl_db_name
        try:
            conn = await asyncpg.connect(settings.connection_string)
        except asyncpg.InvalidCatalogNameError:
            return False
        await conn.close()
        return True

    async def delete(self):
        conn = await self._get_template1_conn()
        try:
            await self._disconnect_all(conn)
            await self._delete(conn)
        finally:
            await conn.close()

    async def recreate(self):
        conn = await self._get_template1_conn()
        try:
            await self._disconnect_all(conn)
            await self._delete(conn)
            await self._create(conn)
        finally:
            await conn.close()

    async def load(self):
        conn = await self._get_template1_conn()
        # noinspection PyBroadException
        try:
            await self._clone_db(conn)
        except Exception:
            await self._delete_cloned_db(conn)
            await self._clone_db(conn)
        finally:
            await conn.close()

    async def clean(self):
        conn = await self._get_template1_conn()
        # noinspection PyBroadException
        try:
            await self._delete_cloned_db(conn)
        finally:
            await conn.close()

    async def restore_from_sql(self):
        if self.dump_sql_filename.exists() is False:
            raise RuntimeError(f"no dump sql found for context {self.context}")
        with open(str(self.dump_sql_filename)) as f:
            sql = f.read()

        await self.recreate()

        conn = await self._get_db_tpl_conn()
        # noinspection PyBroadException
        try:
            await conn.execute(sql)
        finally:
            await conn.close()

    def do_migration(self):
        migrations_path = self.persistence_path.joinpath("migrations")
        if migrations_path.exists() is False:
            raise RuntimeError(f"Migration path for context '{self.context}' not found")
        db_settings = self.settings.db.copy(deep=True)
        db_settings.name = self.tpl_db_name
        MigrationUtils.migrate(db_settings.connection_string, str(migrations_path))

    async def load_initial_data(self):
        if self.has_initial_data() is False:
            raise RuntimeError(f"Initial data not found {self._initial_data_path}")
        # imports the module from the given path
        module = SourceFileLoader(
            "initial_data", str(self._initial_data_path)
        ).load_module()
        settings = self.settings.model_copy(deep=True)
        settings.db.name = self.tpl_db_name
        initial_data = module.InitialDblTplData(settings)
        await initial_data.run()

    async def _delete_cloned_db(self, conn):
        sql = f"DROP DATABASE {self.default_db_name}"
        await conn.execute(sql)

    async def _clone_db(self, conn):
        sql = f"CREATE DATABASE {self.default_db_name} TEMPLATE {self.tpl_db_name}"
        await conn.execute(sql)

    async def _get_template1_conn(self):
        settings = self.settings.db.model_copy(deep=True)
        settings.name = "template1"
        return await asyncpg.connect(settings.connection_string)

    @property
    def _initial_data_path(self) -> Path:
        return self.db_tpl_path.joinpath("initial_db_tpl_data.py")

    async def _create(self, conn):
        sql = f"CREATE DATABASE {self.tpl_db_name}"
        await conn.execute(sql)

    async def _delete(self, conn):
        sql = f"DROP DATABASE IF EXISTS {self.tpl_db_name}"
        await conn.execute(sql)

    async def _get_db_tpl_conn(self):
        settings = self.settings.db.copy(deep=True)
        settings.name = self.tpl_db_name
        return await asyncpg.connect(settings.connection_string)

    async def _disconnect_all(self, conn):
        # noinspection SqlInjection
        sql = (
            "SELECT pg_terminate_backend(pg_stat_activity.pid) "
            "FROM pg_stat_activity "
            f"WHERE pg_stat_activity.datname = '{self.tpl_db_name}' "
            "AND pid <> pg_backend_pid();"
        )
        await conn.execute(sql)
