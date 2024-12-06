from griff.infrastructure.bus.command.abstract_command import (
    AbstractCommand,
    AbstractCommandMiddleware,
    AbstractCommandResponse,
)
from griff.infrastructure.bus.command.command_context import CQContext


class CommandBus(AbstractCommandMiddleware):
    def __init__(self):
        super().__init__()

    async def dispatch(
        self, command: AbstractCommand, context: CQContext = None
    ) -> AbstractCommandResponse:
        if self._next is None:
            # todo: fix couverture des tests manquantes à la prochaine modification
            raise ModuleNotFoundError(
                "Uncomplete middleware chain : Command dispatcher not linked"
            )  # pragma: no cover

        command_response = await self._next.dispatch(command=command, context=context)
        return command_response
