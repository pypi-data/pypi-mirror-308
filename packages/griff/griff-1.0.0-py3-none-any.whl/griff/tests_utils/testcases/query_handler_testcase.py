from abc import ABC, abstractmethod
from typing import Type

from griff.infrastructure.bus.query.abstract_query import AbstractQueryHandler
from griff.services.query_runner.fake_query_runner_service import FakeQueryRunnerService
from griff.tests_utils.testcases.abstract_testcase import AbstractTestCase


class QueryHandlerTestCase(AbstractTestCase, ABC):
    handler: AbstractQueryHandler = None
    fake_query_runner: FakeQueryRunnerService = None
    _extra_handler_dependencies = {}

    @classmethod
    @abstractmethod
    def get_handler_class(cls) -> Type[AbstractQueryHandler]:
        ...

    @classmethod
    def set_handler_extra_dependencies(cls, **extra_handler_dependencies):
        cls._extra_handler_dependencies = extra_handler_dependencies

    def build_query_handler(self) -> AbstractQueryHandler:
        return self.get_handler_class()(
            self.fake_query_runner, **self._extra_handler_dependencies
        )

    @classmethod
    def init_class_context_data(cls):
        pass

    @classmethod
    def init_class_context_services(cls):
        pass

    def init_method_context_data(self):
        self.handler = self.build_query_handler()

    def init_method_context_services(self):
        self.fake_query_runner = FakeQueryRunnerService()
