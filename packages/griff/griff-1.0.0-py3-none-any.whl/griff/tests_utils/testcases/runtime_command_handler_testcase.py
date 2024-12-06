import abc
from typing import Type

from griff.runtime.runtime_factory import RuntimeFactory
from griff.services.uuid.uuid_service import UuidService
from griff.tests_utils.mixins.runtime_test_mixin import RuntimeTestMixin
from griff.tests_utils.testcases.base_testcase import BaseTestCase


class RuntimeDomainHandlerTestCase(RuntimeTestMixin, BaseTestCase):
    @staticmethod
    def get_runtime_factory_class() -> Type[RuntimeFactory]:
        raise NotImplementedError(
            "You must implement get_runtime_factory_class method in your test class"
        )

    @classmethod
    def build_runtime_factory(cls) -> RuntimeFactory:
        runtime_factory = cls.get_runtime_factory_class()()
        return runtime_factory.test_command_handler_runtime(
            additional_injectables=cls.get_additional_injectables(),
        )

    @classmethod
    @abc.abstractmethod
    def get_additional_injectables(cls) -> dict:
        raise NotImplementedError(
            "You must implement get_additional_injectable method in your test class"
        )

    def setup_method(self):
        super().setup_method()
        self.get_runtime_injector().get(UuidService).reset(786)


class RuntimeCommandHandlerTestCase(RuntimeDomainHandlerTestCase):
    @classmethod
    @abc.abstractmethod
    def get_additional_injectables(cls) -> dict:
        raise NotImplementedError(
            "You must implement get_additional_injectable method in your test class"
        )


class RuntimeEventHandlerTestCase(RuntimeDomainHandlerTestCase):
    @classmethod
    @abc.abstractmethod
    def get_additional_injectables(cls) -> dict:
        raise NotImplementedError(
            "You must implement get_additional_injectable method in your test class"
        )
