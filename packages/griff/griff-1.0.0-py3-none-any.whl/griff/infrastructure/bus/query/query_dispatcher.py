from abc import ABC

from griff.infrastructure.bus.middlewares.abstract_middleware import AbstractMiddleware
from griff.infrastructure.bus.query.abstract_query import AbstractQuery
from griff.infrastructure.bus.query.exceptions import QueryBusNoHandlerRegistered


class QueryDispatcher(AbstractMiddleware, ABC):
    def __init__(self):
        super().__init__()
        self.handler_list = dict()

    def has_handler_for(self, query_class):
        return query_class in self.handler_list

    def register_handler(self, query_class, query_handler):
        if query_class in self.handler_list:
            raise SystemError(
                "query handler already registered for " + str(query_class.__name__)
            )

        self.handler_list[query_class] = query_handler

    async def dispatch(self, query: AbstractQuery, context=None):
        """
        The dispatch method of a dispatcher is meant to call the handle method of
        the command handler.
        It is the end of the command chain processing
        """
        if type(query) not in self.handler_list.keys():
            # todo: fix couverture des tests manquantes à la prochaine modification
            raise QueryBusNoHandlerRegistered(
                f"query handler not found for query of type {str(type(query).__name__)}"
            )  # pragma: no cover

        return await self.handler_list[type(query)].handle(query)
