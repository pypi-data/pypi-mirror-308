from injector import inject, singleton

from griff.services.database.database_providers.abstract_db_provider import (
    AbstractDbProvider,
)
from griff.services.database.db_service import DbService


@singleton
class DbTestService(DbService):
    @inject
    def __init__(self, provider: AbstractDbProvider):
        super().__init__(provider)
        self._current_connection = None

    def _get_current_connection(self):
        return self._current_connection

    def _set_current_connection(self, connection):
        self._current_connection = connection
        return None

    def _reset_current_connection(self, token):
        self._current_connection = None
