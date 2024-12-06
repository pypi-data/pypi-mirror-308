from injector import Binder

from griff.runtime.abstract_runtime_component import AsyncRuntimeComponent
from griff.runtime.runtime_environnement import RuntimeEnvironnement
from griff.services.database.database_providers.abstract_db_provider import (
    AbstractDbProvider,
)
from griff.services.database.database_providers.asyncpg_provider import AsyncPgProvider
from griff.services.database.db_service import DbService
from griff.services.database.db_settings import DbSettings
from griff.services.query_runner.query_runner_settings import QueryRunnerSettings
from griff.settings.griff_settings import GriffSettings


class RuntimeDatabase(AsyncRuntimeComponent):
    def __init__(self, settings: GriffSettings, environnement: RuntimeEnvironnement):
        self._settings = settings
        self._runtime = environnement
        self._db_service: DbService = None

    def configure(self, binder: Binder) -> None:
        binder.bind(DbSettings, self._settings.db)
        binder.bind(QueryRunnerSettings, self._settings.query_runner)
        binder.bind(AbstractDbProvider, AsyncPgProvider)

    async def initialize(self):
        await super().initialize()
        injector = self._runtime.get_injector()
        self._db_service = injector.get(DbService)
        await self._db_service.start()

    async def shutdown(self):
        await super().shutdown()
        await self._db_service.stop()
