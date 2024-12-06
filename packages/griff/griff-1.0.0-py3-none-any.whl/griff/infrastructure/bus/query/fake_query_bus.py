from griff.infrastructure.bus.query.abstract_query import AbstractQueryResponse
from griff.infrastructure.bus.query.query_bus import QueryBus


class FakeQueryBus(QueryBus):
    def __init__(self):
        super().__init__()

    async def dispatch(self, event, context=None) -> AbstractQueryResponse:
        return AbstractQueryResponse(msg="dispatched by fake query bus")
