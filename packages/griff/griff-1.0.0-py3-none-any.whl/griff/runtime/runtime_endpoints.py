import importlib
from pathlib import Path

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi_babel import Babel, BabelConfigs
from injector import Binder, singleton
from pydantic_i18n import BabelLoader, PydanticI18n
from starlette.middleware.cors import CORSMiddleware

from griff.exceptions import WError
from griff.infrastructure.registry.meta_endpoint_controller_registry import (
    MetaEndpointControllerRegistry,
)
from griff.infrastructure.registry.meta_registry import MetaEntryPointRegistry
from griff.runtime.abstract_runtime_component import RuntimeComponent
from griff.runtime.fastapi.default_exception_handler_middleware import (
    DefaultExceptionHandlerMiddleware,
)
from griff.runtime.fastapi.pydantic_exception_handler_middleware import (
    PydanticValidationExceptionHandlerMiddleware,
)
from griff.runtime.runtime_environnement import RuntimeEnvironnement


class RuntimeContextEndpoints(RuntimeComponent):
    _is_fast_api_started = False

    def __init__(self, context_name: str, environnement: RuntimeEnvironnement):
        self._runtime = environnement
        # Import du module à partir du nom de variable
        self._context = context_name
        self._context_module = f"DDD.{context_name}.entry_point"
        importlib.import_module(self._context_module)
        self._bounded_contextes = list()
        self._app = None

    @classmethod
    def mark_fast_api_as_started(cls):
        cls._is_fast_api_started = True

    def configure(self, binder: Binder) -> None:
        binder.bind(FastAPI, to=FastAPI, scope=singleton)

    def initialize(self):
        injector = self._runtime.get_injector()
        self._app = injector.get(FastAPI)
        self._runtime.set_fast_api(self._app)
        self._register_contextes(injector)
        self._instanciate_controllers(injector)
        self._start_fastapi()
        RuntimeContextEndpoints.mark_fast_api_as_started()

    def start(self):
        self.register_bounded_contextes_routes()

    def _start_fastapi(self):
        self._app.add_middleware(
            CORSMiddleware, **self._runtime.get_settings().cors_kwargs
        )
        self._app.add_event_handler("startup", self._runtime.async_initialize)
        self._app.add_event_handler("shutdown", self._runtime.async_shutdown)
        self.init_fastapi_locale()
        self.init_pydantic_locale()
        default_exception_handler = DefaultExceptionHandlerMiddleware()
        self._app.add_exception_handler(WError, default_exception_handler.catch)

    def _register_contextes(self, injector):
        for context in MetaEntryPointRegistry.list_types():
            if self._context_module in str(context):
                instance = injector.get(context)
                self._bounded_contextes.append(instance)

    def _instanciate_controllers(self, injector):
        for (
            controller,
            endpoint_list,
        ) in MetaEndpointControllerRegistry.get_endpoint_registry().items():
            injector.get(controller)

    def register_bounded_contextes_routes(self):
        for bounded_context in self._bounded_contextes:
            self._app.include_router(bounded_context.get_router())

    def init_fastapi_locale(self):
        settings = self._runtime.get_settings()
        if settings.locale is None:
            raise RuntimeError("locale setting should be defined, aborting")

        # check translation messages are compiled
        translation_filename = Path(settings.root_dir).joinpath(
            f"{settings.fastapi_local_path}/fr/LC_MESSAGES/messages.mo"
        )
        if translation_filename.exists() is False:
            raise RuntimeError(
                "Translation files are missing, run "
                "`python manage.py locale compilemessages'"
            )

        configs = BabelConfigs(
            ROOT_DIR=settings.root_dir,
            BABEL_DEFAULT_LOCALE=settings.locale.default,
            BABEL_TRANSLATION_DIRECTORY=settings.locale.path,
        )
        babel = Babel(configs=configs)
        babel.init_app(self._app)

    def init_pydantic_locale(self):
        settings = self._runtime.get_settings()
        if settings.locale is None:
            return None
        loader = BabelLoader(f"{settings.pydantic_locale_path}")
        pydantic_i18n = PydanticI18n(loader, default_locale=settings.locale.default)
        pydantic_exc_handler = PydanticValidationExceptionHandlerMiddleware(
            pydantic_i18n
        )
        self._app.add_exception_handler(
            RequestValidationError, pydantic_exc_handler.dispatch
        )
