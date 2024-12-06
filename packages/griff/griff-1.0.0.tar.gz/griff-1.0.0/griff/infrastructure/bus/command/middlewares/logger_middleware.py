from loguru import logger

from griff.infrastructure.bus.command.abstract_command import (
    AbstractCommand,
    AbstractCommandMiddleware,
    AbstractCommandResponse,
)
from griff.infrastructure.bus.command.command_context import CQContext


class LoggerMiddleware(AbstractCommandMiddleware):
    async def dispatch(
        self, command: AbstractCommand, context: CQContext = None
    ) -> AbstractCommandResponse:
        logger.info(f"dispatch command: {command.__class__.__name__}")
        logger.debug(command.model_dump())
        response = await self._next.dispatch(command, context=context)
        logger.debug(response.model_dump())
        return response
