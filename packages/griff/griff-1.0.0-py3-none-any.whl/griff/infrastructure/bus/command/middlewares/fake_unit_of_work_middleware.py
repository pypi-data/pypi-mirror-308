from injector import inject

from griff.infrastructure.bus.command.abstract_command import (
    AbstractCommand,
    AbstractCommandMiddleware,
    AbstractCommandResponse,
)
from griff.infrastructure.bus.command.command_context import CQContext
from griff.services.database.db_service import DbService


class FakeUnitOfWorkMiddleware(AbstractCommandMiddleware):
    @inject
    def __init__(self, db_service: DbService):
        super().__init__()
        self._db_service = db_service

    async def dispatch(
        self, command: AbstractCommand, context: CQContext = None
    ) -> AbstractCommandResponse:
        return await self._next.dispatch(command, context)
