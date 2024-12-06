from typing import List

from griff.services.query_runner.query_runner_service import QueryRunnerService
from griff.tests_utils.mixins.stub_mixin import StubMixin


class FakeQueryRunnerService(StubMixin, QueryRunnerService):
    async def run_query(self, query_name, **query_params):
        return self._call_stub("run_query")

    async def run_many_query(self, query_name, queries_params: List[dict]):
        return self._call_stub("run_many_query")

    def set_sql_queries(self, relative_sql_path: str) -> None:
        self._call_stub("set_sql_queries")
