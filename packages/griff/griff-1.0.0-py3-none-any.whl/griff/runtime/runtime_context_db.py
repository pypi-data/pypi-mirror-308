from injector import Binder

from griff.runtime.runtime_db import RuntimeDatabase
from griff.services.database.db_service import DbService
from griff.services.database.db_test_service import DbTestService
from griff.settings.griff_settings import GriffSettings
from griff.tests_utils.db_tpl_utils import DbTplUtils


class RuntimeContextDatabase(RuntimeDatabase):
    def __init__(self, settings: GriffSettings, context_name: str, environnement):
        super().__init__(settings, environnement)
        self.tpl_utils = DbTplUtils(
            context=context_name, settings=environnement.get_settings()
        )

    def configure(self, binder: Binder) -> None:
        super().configure(binder)
        binder.bind(DbService, DbTestService)

    async def initialize(self):
        await self.tpl_utils.load()
        await super().initialize()

    async def start(self):
        await self._db_service.start_transaction()

    async def stop(self):
        await self._db_service.rollback_transaction()

    async def shutdown(self):
        await super().shutdown()
        await self.tpl_utils.clean()
