from injector import Binder

from griff.runtime.abstract_runtime_component import RuntimeComponent
from griff.services.query_runner.query_runner_settings import QueryRunnerSettings


class RuntimeQueryRunner(RuntimeComponent):
    def __init__(self, settings: QueryRunnerSettings):
        self._settings = settings

    def configure(self, binder: Binder) -> None:
        binder.bind(QueryRunnerSettings, self._settings)
