from griff.infrastructure.bus.command.abstract_command import (
    AbstractCommand,
    AbstractCommandResponse,
)
from griff.infrastructure.bus.command.command_bus import CommandBus


class FakeCommandBus(CommandBus):
    def __init__(self):
        super().__init__(event_bus=None)

    async def dispatch(
        self, command: AbstractCommand, context=None
    ) -> AbstractCommandResponse:
        return AbstractCommandResponse(msg="dispatched by fake command bus")
