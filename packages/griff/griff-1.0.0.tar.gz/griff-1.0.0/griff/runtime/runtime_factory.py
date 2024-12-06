import sys
from abc import ABC
from typing import Type

from loguru import logger
from typing_extensions import deprecated

from griff.infrastructure.bus.command.command_bus import CommandBus
from griff.infrastructure.bus.command.fake_command_bus import FakeCommandBus
from griff.infrastructure.bus.command.middlewares.fake_unit_of_work_middleware import (
    FakeUnitOfWorkMiddleware,
)
from griff.infrastructure.bus.command.middlewares.unit_of_work_middleware import (
    UnitOfWorkMiddleware,
)
from griff.infrastructure.bus.query.fake_query_bus import FakeQueryBus
from griff.infrastructure.bus.query.query_bus import QueryBus
from griff.runtime.runtime_cli_command import RuntimeCliCommand
from griff.runtime.runtime_command_bus import RuntimeCommandBus
from griff.runtime.runtime_context_db import RuntimeContextDatabase
from griff.runtime.runtime_db import RuntimeDatabase
from griff.runtime.runtime_endpoints import RuntimeContextEndpoints
from griff.runtime.runtime_environnement import RuntimeEnvironnement
from griff.runtime.runtime_injectable import RuntimeInjectable
from griff.runtime.runtime_query_bus import RuntimeQueryBus
from griff.runtime.runtime_query_runner import RuntimeQueryRunner
from griff.services.database.db_settings import DbSettings
from griff.services.date.date_service import DateService
from griff.services.date.fake_date_service import FakeDateService
from griff.services.jwt.jwt_settings import JwtSettings
from griff.services.mail.mail_settings import MailSettings
from griff.services.query_runner.query_runner_settings import QueryRunnerSettings
from griff.services.template.renderers.abstract_template_renderer import (
    AbstractTemplateRenderer,
)
from griff.services.template.renderers.jinja2_template_renderer import (
    Jinja2TemplateRenderer,
)
from griff.services.template.template_settings import TemplateSettings
from griff.services.token.fake_token_service import FakeTokenService
from griff.services.token.token_service import TokenService
from griff.services.uuid.fake_uuid_service import FakeUuidService
from griff.services.uuid.uuid_service import UuidService
from griff.settings.griff_settings import GriffSettings, LogLevel


class RuntimeFactory(ABC):
    def __init__(self, env: str = None):
        self._rte = None
        self._env = env

    def _runtime(self):
        self._rte = RuntimeEnvironnement()
        return self

    def test_base_runtime(self) -> "RuntimeFactory":
        return (
            self._runtime()
            .with_settings()
            .with_log_level()
            .with_service_settings()
            .with_fake_default_services()
            .with_custom_injectable(UuidService, FakeUuidService(100))
            .with_custom_injectable(TokenService, FakeTokenService(900))
            .with_custom_injectable(DateService, FakeDateService())
        )

    def _test_customized_domain_runtime(
        self, additional_injectables: dict
    ) -> "RuntimeFactory":
        base_runtime = self.test_base_runtime()
        for abstract_type, real_type in additional_injectables.items():
            base_runtime = base_runtime.with_custom_injectable(abstract_type, real_type)
        return base_runtime

    def test_repository_runtime(self, bounded_context) -> "RuntimeFactory":
        return self.test_base_runtime().with_context_db(bounded_context)

    def test_command_handler_runtime(
        self, additional_injectables: dict
    ) -> "RuntimeFactory":
        return self._test_customized_domain_runtime(additional_injectables)

    def test_event_handler_runtime(
        self, additional_injectables: dict
    ) -> "RuntimeFactory":
        return self._test_customized_domain_runtime(additional_injectables)

    def test_api_runtime(self, bounded_context) -> "RuntimeFactory":
        return (
            self.test_repository_runtime(bounded_context)
            .with_log_level()
            .with_event_bus()
            .with_command_bus()
            .with_query_bus()
            .with_query_runner()
            .with_context_endpoints(bounded_context)
            .with_custom_injectable(UnitOfWorkMiddleware, FakeUnitOfWorkMiddleware)
        )

    @deprecated("use dedicated test_base_runtime instead")
    def test_runtime(self) -> "RuntimeFactory":
        return (
            self._runtime()
            .with_settings()
            .with_log_level()
            .with_common_cli_commands()
            .with_service_settings()
            .with_fake_default_services()
            .with_event_bus()
            .with_command_bus()
            .with_query_bus()
        )

    def web_runtime(self) -> "RuntimeFactory":  # pragma no cover
        return (
            self._runtime()
            .with_settings()
            .with_log_level()
            .with_all_endpoints()
            .with_service_settings()
            .with_command_bus()
            .with_event_bus()
            .with_query_bus()
            .with_full_db()
            .with_query_runner()
        )

    def cli_runtime(self) -> "RuntimeFactory":  # pragma no cover
        return (
            self._runtime()
            .with_settings()
            .with_log_level()
            .with_common_cli_commands()
            .with_service_settings()
            .with_command_bus()
            .with_event_bus()
            .with_query_bus()
            .with_full_db()
            .with_query_runner()
        )

    def with_full_db(self) -> "RuntimeFactory":  # pragma no cover
        self._rte.check_is_set()
        prod_db = RuntimeDatabase(
            settings=self._rte.get_settings(),
            environnement=self._rte,
        )
        self._rte.add_component(prod_db)
        return self

    def with_all_endpoints(self):  # pragma no cover
        raise NotImplementedError(
            "with all endpoint method shall be implemented by app runtime factory"
        )

    def with_cli_commands(self):
        raise NotImplementedError(
            "with all cli command method shall be implemented by app runtime factory"
        )

    def with_common_cli_commands(self) -> "RuntimeFactory":
        runtime_endpoints = RuntimeCliCommand(
            context_name=None, environnement=self._rte
        )
        self._rte.add_component(runtime_endpoints)
        return self

    def with_context_cli_commands(self, context_name: str) -> "RuntimeFactory":
        runtime_endpoints = RuntimeCliCommand(
            context_name=context_name, environnement=self._rte
        )
        self._rte.add_component(runtime_endpoints)
        return self

    def with_settings(
        self, settings_klass: Type = GriffSettings, settings: GriffSettings = None
    ) -> "RuntimeFactory":
        if self._rte._settings is not None:
            raise RuntimeError("Setting already set on runtime")
        if settings is None:
            settings = settings_klass()
        rs = RuntimeInjectable(settings_klass, settings)
        rig = RuntimeInjectable(GriffSettings, settings)
        self._rte.set_settings(settings)
        self._rte.add_component(rs)
        self._rte.add_component(rig)
        return self

    def with_query_runner(self) -> "RuntimeFactory":
        query_runner = RuntimeQueryRunner(self._rte.get_settings().query_runner)
        self._rte.add_component(query_runner)
        return self

    def with_context_db(self, context_name: str) -> "RuntimeFactory":
        self._rte.check_is_set()
        context_db = RuntimeContextDatabase(
            settings=self._rte.get_settings(),
            context_name=context_name,
            environnement=self._rte,
        )
        self._rte.add_component(context_db)
        return self

    def with_command_bus(self) -> "RuntimeFactory":
        command_bus = RuntimeCommandBus(environnement=self._rte)
        self._rte.add_component(command_bus)
        return self

    def with_query_bus(self) -> "RuntimeFactory":
        query_bus = RuntimeQueryBus(environnement=self._rte)
        self._rte.add_component(query_bus)
        return self

    def with_event_bus(self) -> "RuntimeFactory":
        return self

    def with_service(self, service_type: type, service_instance) -> "RuntimeFactory":
        rs = RuntimeInjectable(service_type, service_instance)
        self._rte.add_component(rs)
        return self

    def with_fake_default_services(self) -> "RuntimeFactory":
        self.with_service(DateService, FakeDateService)
        return self

    def with_service_settings(self) -> "RuntimeFactory":
        self.with_service(JwtSettings, self._rte._settings.jwt)
        self.with_service(MailSettings, self._rte._settings.mail)
        self.with_service(TemplateSettings, self._rte._settings.template)
        self.with_service(QueryRunnerSettings, self._rte._settings.query_runner)
        self.with_service(DbSettings, self._rte._settings.db)
        self.with_service(AbstractTemplateRenderer, Jinja2TemplateRenderer)
        return self

    def with_custom_injectable(
        self, service_type, service_instance
    ) -> "RuntimeFactory":
        rs = RuntimeInjectable(service_type, service_instance)
        self._rte.replace_runtime_injectable(rs)
        return self

    def build(self) -> RuntimeEnvironnement:
        return self._rte.create()

    def with_context_endpoints(self, context_name: str) -> "RuntimeFactory":
        runtime_endpoints = RuntimeContextEndpoints(
            context_name=context_name, environnement=self._rte
        )
        self._rte.add_component(runtime_endpoints)
        return self

    def with_fake_command_bus(self) -> "RuntimeFactory":
        rs = RuntimeInjectable(CommandBus, FakeCommandBus)
        self._rte.add_component(rs)
        return self

    def with_fake_event_bus(self) -> "RuntimeFactory":
        return self

    def with_fake_query_bus(self) -> "RuntimeFactory":  # pragma no cover
        rs = RuntimeInjectable(QueryBus, FakeQueryBus)
        self._rte.add_component(rs)
        return self

    def with_log_level(self, log_level: LogLevel = None) -> "RuntimeFactory":
        logger.remove()
        log_level = (
            log_level if log_level is not None else self._rte._settings.log_level.value
        )
        logger.add(sys.stderr, level=log_level)
        return self
