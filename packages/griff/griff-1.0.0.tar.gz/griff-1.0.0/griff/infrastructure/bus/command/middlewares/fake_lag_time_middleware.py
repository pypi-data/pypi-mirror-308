import asyncio
import random

from loguru import logger

from griff.infrastructure.bus.command.abstract_command import (
    AbstractCommand,
    AbstractCommandMiddleware,
    AbstractCommandResponse,
)
from griff.infrastructure.bus.command.command_context import CQContext


class FakeLagTimeMiddleware(AbstractCommandMiddleware):
    """
    simulate response lag
    """

    async def dispatch(
        self, command: AbstractCommand, context: CQContext = None
    ) -> AbstractCommandResponse:
        durations = [0, 0.3, 0.5, 0.5, 0.5, 0.5, 0.6, 0.8, 0.8, 1]
        sleep_duration = random.choice(durations)
        if sleep_duration > 0:
            logger.info(f"Fake lag time of {sleep_duration}s ...")
            await asyncio.sleep(sleep_duration)
            logger.info("Fake lag time over")
        else:
            logger.info("Retarder ignored")
        return await self._next.dispatch(command, context=context)
