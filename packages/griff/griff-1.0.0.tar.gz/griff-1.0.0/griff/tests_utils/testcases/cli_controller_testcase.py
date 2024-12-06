from abc import abstractmethod
from typing import Type

from griff.infrastructure.cli.abstract.abstract_cli_controller import (
    AbstractCliController,
)
from griff.runtime.runtime_factory import RuntimeFactory
from griff.tests_utils.mixins.runtime_test_mixin import RuntimeTestMixin
from griff.tests_utils.testcases.abstract_testcase import AbstractTestCase


class CliControllerTestCase(RuntimeTestMixin, AbstractTestCase):
    @classmethod
    @abstractmethod
    def get_controller_cli_class(cls) -> Type[AbstractCliController]:
        ...

    @classmethod
    def build_runtime_factory(cls) -> RuntimeFactory:
        return RuntimeFactory().test_base_runtime()

    @classmethod
    def init_class_context_data(cls):
        cls.controller = cls.get_runtime_injected(cls.get_controller_cli_class())

    @classmethod
    def init_class_context_services(cls):
        pass

    def init_method_context_data(self):
        pass

    def init_method_context_services(self):
        pass
