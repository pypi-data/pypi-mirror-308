from injector import singleton

from griff.infrastructure.bus.command.abstract_command import (
    AbstractCommand,
    AbstractCommandMiddleware,
    AbstractCommandResponse,
)
from griff.infrastructure.bus.event.abstract_event import AbstractEvent


@singleton
class EventDispatchMiddleware(AbstractCommandMiddleware):
    def __init__(self):
        super().__init__()
        self.handler_list = dict()

    def has_handler_for(self, event_class):
        return event_class in self.handler_list.keys()

    def register_handler(self, event_class, event_handler) -> int:
        if event_class not in self.handler_list:
            self.handler_list[event_class] = list()

        if event_handler.__class__ in [
            handler.__class__ for handler in self.handler_list[event_class]
        ]:
            return len(self.handler_list[event_class])

        self.handler_list[event_class].append(event_handler)
        self.handler_list[event_class].sort(
            key=lambda elem: str(elem.__class__.__module__)
        )

        return len(self.handler_list[event_class])

    async def _dispatch_event(self, event: AbstractEvent, context=None) -> None:
        if type(event) not in self.handler_list.keys():
            return None

        if len(self.handler_list[type(event)]) == 0:
            # todo: fix couverture des tests manquantes à la prochaine modification
            return None  # pragma: no cover

        for handler in self.handler_list[type(event)]:
            await handler.handle(event, context=context)

    async def dispatch(
        self, command: AbstractCommand, context=None
    ) -> AbstractCommandResponse:
        response = await self._next.dispatch(command, context=context)

        if response.linked_events is None or len(response.linked_events) == 0:
            return response

        for event in response.linked_events:
            await self._dispatch_event(event, context=context)

        return response
