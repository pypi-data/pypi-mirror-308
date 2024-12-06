from injector import inject

from griff.infrastructure.bus.command.abstract_command import (
    AbstractCommand,
    AbstractCommandMiddleware,
    AbstractCommandResponse,
)
from griff.infrastructure.bus.command.command_context import CQContext
from griff.services.database.db_service import DbService


class UnitOfWorkMiddleware(AbstractCommandMiddleware):
    @inject
    def __init__(self, db_service: DbService):
        super().__init__()
        self._db_service = db_service

    async def dispatch(
        self, command: AbstractCommand, context: CQContext = None
    ) -> AbstractCommandResponse:
        response = None
        async with self._db_service.transaction():
            if self._next:
                response = await self._next.dispatch(command, context=context)
            return response
