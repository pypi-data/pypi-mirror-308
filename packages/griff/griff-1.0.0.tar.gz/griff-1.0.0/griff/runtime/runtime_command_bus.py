from injector import Binder, provider, singleton

from griff.infrastructure.bus.command.command_bus import CommandBus
from griff.infrastructure.bus.command.command_dispatcher import CommandDispatcher
from griff.infrastructure.bus.command.middlewares.event_middleware import (
    EventDispatchMiddleware,
)
from griff.infrastructure.bus.command.middlewares.logger_middleware import (
    LoggerMiddleware,
)
from griff.infrastructure.bus.command.middlewares.unit_of_work_middleware import (
    UnitOfWorkMiddleware,
)
from griff.infrastructure.registry.meta_registry import (
    MetaCommandHandlerRegistry,
    MetaEventHandlerRegistry,
)
from griff.runtime.abstract_runtime_component import RuntimeComponent


class RuntimeCommandBus(RuntimeComponent):
    def __init__(self, environnement):
        self._runtime = environnement

    def configure(self, binder: Binder) -> None:
        binder.bind(CommandDispatcher, CommandDispatcher, scope=singleton)

    @provider
    def build_command_bus(
        self,
        command_dispatcher: CommandDispatcher,
        event_dispatch_mw: EventDispatchMiddleware,
        uow: UnitOfWorkMiddleware,
        logger: LoggerMiddleware,
    ) -> CommandBus:
        cmd_bus = CommandBus()
        cmd_bus.set_next(logger)
        logger.set_next(uow)
        uow.set_next(event_dispatch_mw)
        event_dispatch_mw.set_next(command_dispatcher)
        return cmd_bus

    def _init_command_dispatcher(self):
        handler_list = MetaCommandHandlerRegistry.list_types()
        injector = self._runtime.get_injector()
        for handler_type in handler_list:
            dispatcher = injector.get(CommandDispatcher)
            if handler_type.listen_to() is None:
                continue

            if dispatcher.has_handler_for(handler_type.listen_to()):
                continue

            dispatcher.register_handler(
                handler_type.listen_to(), injector.get(handler_type)
            )

    def _init_event_dispatcher(self):
        handler_list = MetaEventHandlerRegistry.list_types()
        injector = self._runtime.get_injector()
        for handler_type in handler_list:
            event_dispatcher = injector.get(EventDispatchMiddleware)
            if handler_type.listen_to() is None:
                continue

            event_dispatcher.register_handler(
                handler_type.listen_to(), injector.get(handler_type)
            )

    def start(self):
        self._init_command_dispatcher()
        self._init_event_dispatcher()
