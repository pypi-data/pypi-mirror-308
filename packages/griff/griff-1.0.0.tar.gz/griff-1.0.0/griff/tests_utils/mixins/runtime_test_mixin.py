import abc
from typing import Type, TypeVar

from injector import Injector

from griff.runtime.runtime_environnement import RuntimeEnvironnement
from griff.runtime.runtime_factory import RuntimeFactory
from griff.settings.griff_settings import GriffSettings
from griff.tests_utils.mixins.async_test_mixin import AsyncTestMixin

T = TypeVar("T")


class RuntimeTestMixin(AsyncTestMixin, abc.ABC):
    _runtime: RuntimeEnvironnement

    @classmethod
    @abc.abstractmethod
    def build_runtime_factory(cls) -> RuntimeFactory:
        ...

    @classmethod
    def setup_class(cls):
        cls._runtime = cls.build_runtime_factory().build()
        cls._runtime.initialize()
        cls.settings = cls._runtime.get_settings()
        if hasattr(super(), "setup_class"):
            super().setup_class()

    @classmethod
    def teardown_class(cls):
        cls._runtime.shutdown()
        cls._runtime = None

    def setup_method(self):
        self._runtime.start()
        if hasattr(super(), "setup_method"):
            super().setup_method()

    def teardown_method(self):
        if hasattr(super(), "teardown_method"):
            super().teardown_method()
        self._runtime.stop()

    async def async_setup_class(self):
        await self._runtime.async_initialize()

    async def async_teardown_class(self):
        await self._runtime.async_shutdown()

    async def async_setup(self):
        await self._runtime.async_start()

    async def async_teardown(self):
        await self._runtime.async_stop()

    @classmethod
    def get_runtime(cls) -> RuntimeEnvironnement:
        return cls._runtime

    @classmethod
    def get_runtime_injector(cls) -> Injector:
        return cls._runtime.get_injector()

    @classmethod
    def get_runtime_injected(cls, klass_name: Type[T]) -> T:
        return cls._runtime.get_injector().get(klass_name)

    @classmethod
    def get_runtime_settings(cls) -> GriffSettings:
        return cls._runtime.get_settings()
