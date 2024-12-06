import glob
import os

import asyncpg
import typer
from injector import inject

from griff.infrastructure.cli.abstract.abstract_db_cli_controller import (
    AbstractDbCliController,
)
from griff.infrastructure.cli.abstract.register_cli_command import register_cli_command
from griff.infrastructure.cli.commands.typer_print import TyperPrint
from griff.settings.griff_settings import GriffSettings
from griff.tests_utils.db_tpl_utils import DbTplUtils
from griff.utils.async_utils import AsyncUtils
from griff.utils.migration_utils import MigrationUtils


class DBCliController(AbstractDbCliController):
    @inject
    def __init__(self, settings: GriffSettings):
        super().__init__(settings)

    def get_command_name(self):
        return "bdd"

    def _get_migrations_dir(self, domain_name: str) -> str:
        return str(self._settings.get_migration_path(domain_name))

    @register_cli_command(name="init_bdd")
    def initialize_bdd(self, noinput: bool = False):
        if noinput is False:
            confirmed = typer.confirm(
                f"It will erase entire database "
                f"'{self._settings.db.name}', are you sure?"
            )
            if not confirmed:
                TyperPrint.warning("Ok, no pb, see you later !!")
                raise typer.Exit()
        TyperPrint.info("Init Bdd")

        AsyncUtils.async_to_sync(self._recreate_db)

        self._do_migrations()

        if self._settings.env in ["dev", "pytest"]:
            self.initialize_db_tpl()

        TyperPrint.success("DONE")

    @register_cli_command(name="init_tpl")
    def initialize_db_tpl(self):
        if self._settings.env not in ["dev", "pytest"]:
            TyperPrint.error(f"command forbidden in '{self._settings.env}' environment")
            raise typer.Exit()
        TyperPrint.info("Init Db Templates")
        AsyncUtils.async_to_sync(self._recreate_db_tpl)
        TyperPrint.success("DONE")

    @register_cli_command(name="migrate")
    def migrate(self):
        self._do_migrations()

    @register_cli_command(name="makemigrations")
    def make_migrations(self, domain_name: str):
        os.system(f"yoyo new --sql {self._get_migrations_dir(domain_name)}")

    async def _recreate_db(self):
        settings = self._settings.db.model_copy(deep=True)
        settings.name = "template1"
        await self._disconnect_all(settings)
        conn = await asyncpg.connect(settings.connection_string)
        try:
            # noinspection TryExceptPass
            try:
                await self._drop_db(conn)
            except Exception:
                pass
            await self._create_db(conn)
        finally:
            await conn.close()

    async def _recreate_db_tpl(self):
        pattern = "DDD/[!_]*/"
        for context_path in glob.glob(pattern, root_dir=self._settings.root_dir):
            context = context_path.split("/")[1]
            await self._restore(DbTplUtils(context, self._settings))

    async def _disconnect_all(self, settings):
        TyperPrint.info("  disconnect all ...", with_newline=False)
        conn = await asyncpg.connect(settings.connection_string)
        try:
            # noinspection SqlInjection
            sql = (
                "SELECT pg_terminate_backend(pg_stat_activity.pid) "
                "FROM pg_stat_activity "
                f"WHERE pg_stat_activity.datname = '{self._settings.db.name}' "
                "AND pid <> pg_backend_pid();"
            )
            await conn.execute(sql)
        except Exception as e:
            TyperPrint.error(f"  {e}")
            raise typer.Exit()
        TyperPrint.info("  Ok")

    async def _create_db(self, conn):
        TyperPrint.info("  creating db ...", with_newline=False)
        try:
            # noinspection SqlInjection
            sql = f"CREATE DATABASE {self._settings.db.name}"
            await conn.execute(sql)
        except Exception as e:
            TyperPrint.error(f"  {e}")
            raise typer.Exit()
        TyperPrint.info("  Ok")

    async def _drop_db(self, conn):
        TyperPrint.info("  droping db ...", with_newline=False)
        try:
            # noinspection SqlInjection
            sql = f"DROP DATABASE {self._settings.db.name}"
            await conn.execute(sql)
        except Exception as e:
            TyperPrint.error(f"  {e}")
            raise typer.Exit()
        TyperPrint.info("  Ok")

    def _do_migrations(self):
        pattern = self._get_migrations_dir("[!_]*")
        for migration_path in glob.glob(pattern, root_dir=self._settings.root_dir):
            context = migration_path.split("/")[1]
            TyperPrint.info(
                f"  applying migration(s) for {context} ...", with_newline=False
            )
            MigrationUtils.migrate(self._settings.db.connection_string, migration_path)
            TyperPrint.info("  Ok")
