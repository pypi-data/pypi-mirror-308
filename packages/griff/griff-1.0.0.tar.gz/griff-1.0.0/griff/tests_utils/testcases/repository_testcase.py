from abc import ABC, abstractmethod
from typing import Type

from griff.domain.auto_vo.abstract_aggregate_root import AbstractAggregateFactory
from griff.infrastructure.persistence.repository.abstract_base_repository import (
    AbstractBaseRepository,
)
from griff.runtime.runtime_factory import RuntimeFactory
from griff.services.date.date_service import DateService
from griff.services.uuid.fake_uuid_service import FakeUuidService
from griff.services.uuid.uuid_service import UuidService
from griff.tests_utils.mixins.runtime_test_mixin import RuntimeTestMixin
from griff.tests_utils.testcases.abstract_testcase import AbstractTestCase


class RepositoryTestCase(RuntimeTestMixin, AbstractTestCase, ABC):
    factory: AbstractAggregateFactory
    fake_uuid_service: FakeUuidService

    @classmethod
    def init_class_context_data(cls):
        cls.factory = cls.build_aggregate_factory()
        cls.repository = cls.get_runtime_injected(cls.get_repository_class())

    @classmethod
    def init_class_context_services(cls):
        # noinspection PyTypeChecker
        cls.fake_uuid_service = cls.get_runtime_injected(UuidService)
        cls.fake_uuid_service.reset(1000123)

    def init_method_context_data(self):
        self.fake_uuid_service.reset(763)

    def init_method_context_services(self):
        pass

    def get_aggregate_factory(self) -> AbstractAggregateFactory:
        return self.factory

    @classmethod
    def build_runtime_factory(cls) -> RuntimeFactory:
        runtime_factory = cls.get_runtime_factory_class()()
        return runtime_factory.test_repository_runtime(
            bounded_context=cls.get_bounded_context()
        )

    @classmethod
    def build_aggregate_factory(cls) -> AbstractAggregateFactory:
        # noinspection PyArgumentList
        return cls.get_aggregate_factory_class()(
            date_service=cls.get_runtime_injector().get(DateService),
            uuid_service=cls.fake_uuid_service,
        )

    @staticmethod
    @abstractmethod
    def get_runtime_factory_class() -> Type[RuntimeFactory]:
        ...

    @staticmethod
    @abstractmethod
    def get_repository_class() -> Type[AbstractBaseRepository]:
        ...

    @staticmethod
    @abstractmethod
    def get_bounded_context() -> str:
        ...

    @staticmethod
    @abstractmethod
    def get_aggregate_factory_class() -> Type[AbstractAggregateFactory]:
        ...
