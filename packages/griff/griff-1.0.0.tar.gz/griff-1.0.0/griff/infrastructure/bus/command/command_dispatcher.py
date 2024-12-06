from abc import ABC

from griff.infrastructure.bus.command.abstract_command import (
    AbstractCommand,
    AbstractCommandMiddleware,
    AbstractCommandResponse,
)
from griff.infrastructure.bus.command.command_context import CQContext


class CommandDispatcher(AbstractCommandMiddleware, ABC):
    def __init__(self):
        super().__init__()
        self.handler_list = dict()

    def has_handler_for(self, command_class):
        return command_class in self.handler_list

    def register_handler(self, command_class, command_handler):
        if command_class in self.handler_list:
            raise SystemError(
                "command handler already registered for " + str(command_class.__name__)
            )

        self.handler_list[command_class] = command_handler

    async def dispatch(
        self, command: AbstractCommand, context: CQContext = None
    ) -> AbstractCommandResponse:
        """
        The dispatch method of a dispatcher is meant to call the handle method of the
        command handler.
        It is the end of the command chain processing
        """
        if type(command) not in self.handler_list.keys():
            # todo: fix couverture des tests manquantes à la prochaine modification
            raise ModuleNotFoundError(
                "command handler not found for command of type "
                + str(type(command).__name__)
            )  # pragma: no cover

        response = await self.handler_list[type(command)].handle(
            command=command, context=context
        )
        return response
