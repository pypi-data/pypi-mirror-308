from typing import Type

from griff.domain.auto_vo.abstract_aggregate_root import AbstractAggregateFactory
from griff.infrastructure.bus.command.abstract_command import AbstractCommandHandler
from griff.infrastructure.persistence.repository.abstract_base_repository import (
    AbstractBaseRepository,
)
from griff.services.date.fake_date_service import FakeDateService
from griff.services.uuid.fake_uuid_service import FakeUuidService
from griff.tests_utils.testcases.abstract_testcase import AbstractTestCase


class CommandHandlerTestCase(AbstractTestCase):
    _uuid_service: FakeUuidService
    _date_service: FakeDateService
    _aggregate_factory: AbstractAggregateFactory
    _fake_repository: AbstractBaseRepository
    _command_handler: AbstractCommandHandler
    _extra_handler_dependencies: dict = {}

    @classmethod
    def init_class_context_services(cls):
        super().init_class_context_services()
        cls._uuid_service = FakeUuidService(890)
        cls._date_service = FakeDateService()

    @classmethod
    def init_class_context_data(cls):
        super().init_class_context_data()
        cls.build_aggregate_factory()
        cls.build_fake_repository()
        cls.build_handler()

    def init_method_context_data(self):
        pass

    def init_method_context_services(self):
        self._uuid_service.reset(786)
        self._fake_repository._persistance_adapter.reset()

    @classmethod
    def build_aggregate_factory(cls):
        if hasattr(cls, "aggregate_root"):
            """deprecated"""
            return cls._deprecated_build_aggregate_factory()

        cls._aggregate_factory = cls.get_aggregate_factory_class()(
            uuid_service=cls._uuid_service, date_service=cls._date_service
        )

    @classmethod
    def build_fake_repository(cls):
        cls._fake_repository = cls.get_fake_repository_class()(
            aggregate_factory=cls._aggregate_factory,
            date_service=cls._date_service,
        )

    @classmethod
    def build_handler(cls):
        cls._command_handler = cls.get_command_handler_class()(
            repository=cls._fake_repository, **cls._extra_handler_dependencies
        )

    @classmethod
    def get_aggregate_factory_class(cls) -> Type[AbstractAggregateFactory]:
        raise NotImplementedError(
            "You need to implement 'get_aggregate_factory_class' method"
        )

    @classmethod
    def get_fake_repository_class(cls) -> Type[AbstractBaseRepository]:
        if hasattr(cls, "repository"):
            """deprecated"""
            return cls.repository
        raise NotImplementedError(
            "You need to implement 'get_fake_repository_class' method"
        )

    @classmethod
    def get_command_handler_class(cls) -> Type[AbstractCommandHandler]:
        if hasattr(cls, "command_handler"):
            """deprecated"""
            cls.set_handler_extra_dependencies(
                uuid_service=cls._uuid_service, date_service=cls._date_service
            )
            return cls.command_handler
        raise NotImplementedError(
            "You need to implement 'get_command_handler_class' method"
        )

    @classmethod
    def set_handler_extra_dependencies(cls, **extra_handler_dependencies):
        cls._extra_handler_dependencies = extra_handler_dependencies

    @classmethod
    def _deprecated_build_aggregate_factory(cls):
        """deprecated"""
        cls._aggregate_factory = cls.aggregate_root.factory(
            services=[cls._uuid_service, cls._date_service]
        )
