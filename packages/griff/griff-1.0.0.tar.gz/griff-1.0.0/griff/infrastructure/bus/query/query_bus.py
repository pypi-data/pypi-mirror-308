from griff.infrastructure.bus.middlewares.abstract_middleware import AbstractMiddleware
from griff.infrastructure.bus.query.abstract_query import AbstractQueryResponse


class QueryBus(AbstractMiddleware):
    def __init__(self):
        super().__init__()

    async def dispatch(self, event, context=None) -> AbstractQueryResponse:
        if self._next:
            return await self._next.dispatch(event, context=context)

        # todo: fix couverture des tests manquantes à la prochaine modification
        raise ModuleNotFoundError(
            "Uncomplete middleware chain : query dispatcher not linked"
        )  # pragma: no cover
