from injector import Binder, provider, singleton
from loguru import logger

from griff.infrastructure.bus.command.middlewares.logger_middleware import (
    LoggerMiddleware,
)
from griff.infrastructure.bus.query.query_bus import QueryBus
from griff.infrastructure.bus.query.query_dispatcher import QueryDispatcher
from griff.infrastructure.registry.meta_registry import MetaQueryHandlerRegistry
from griff.runtime.abstract_runtime_component import RuntimeComponent


class RuntimeQueryBus(RuntimeComponent):
    def __init__(self, environnement):
        self._runtime = environnement

    def configure(self, binder: Binder) -> None:
        binder.bind(QueryDispatcher, QueryDispatcher, scope=singleton)

    @singleton
    @provider
    def build_query_bus(
        self,
        query_dispatcher: QueryDispatcher,
        logger: LoggerMiddleware,
    ) -> QueryBus:
        query_bus = QueryBus()
        query_bus.set_next(logger)
        logger.set_next(query_dispatcher)
        return query_bus

    def start(self):
        handler_list = MetaQueryHandlerRegistry.list_types()
        injector = self._runtime.get_injector()
        for handler_type in handler_list:
            logger.debug(handler_type)
            dispatcher = injector.get(QueryDispatcher)
            if handler_type.listen_to() is None:
                continue

            if dispatcher.has_handler_for(handler_type.listen_to()):
                continue

            dispatcher.register_handler(
                handler_type.listen_to(), injector.get(handler_type)
            )
