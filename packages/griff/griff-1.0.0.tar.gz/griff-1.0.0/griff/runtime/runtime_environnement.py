from typing import List

from fastapi import FastAPI
from injector import Injector, Module
from typer import Typer

from griff.runtime.abstract_runtime_component import (
    AsyncRunnableComponent,
    AsyncRuntimeComponent,
    RunnableComponents,
    RuntimeComponent,
)
from griff.runtime.runtime_injectable import RuntimeInjectable
from griff.settings.griff_settings import GriffSettings


class RuntimeEnvironnement:
    def __init__(self):
        self._settings: GriffSettings | None = None
        self._injector = None
        self._app: FastAPI = None
        self._typer: Typer = None
        self._is_finalized: bool = False
        self._components: List[RuntimeComponent | Module | RunnableComponents] = list()
        self._async_components: List[
            AsyncRuntimeComponent | Module | AsyncRunnableComponent
        ] = list()

    async def async_initialize(self):
        for component in self._async_components:
            if issubclass(type(component), AsyncRunnableComponent):
                await component.initialize()

    async def async_start(self):
        for component in self._async_components:
            if issubclass(type(component), AsyncRunnableComponent):
                await component.start()

    async def async_stop(self):
        for component in self._async_components:
            if issubclass(type(component), AsyncRunnableComponent):
                await component.stop()

    async def async_shutdown(self):
        for component in self._async_components:
            if issubclass(type(component), AsyncRunnableComponent):
                await component.shutdown()

    def initialize(self):
        for component in self._components:
            if issubclass(type(component), RunnableComponents):
                component.initialize()

    def start(self):
        for component in self._components:
            if issubclass(type(component), RunnableComponents):
                component.start()

    def stop(self):
        for component in self._components:
            if issubclass(type(component), RunnableComponents):
                component.stop()

    def shutdown(self):
        for component in self._components:
            if issubclass(type(component), RunnableComponents):
                component.shutdown()

    def check_is_set(self):
        if self._settings is None:
            raise RuntimeError(
                "Setting shall be initialized first when creating a runtime config"
            )

    def get_fast_api(self) -> FastAPI:
        return self._app

    def set_fast_api(self, app: FastAPI):
        self._app = app

    def get_typer(self) -> Typer:
        return self._typer

    def set_typer(self, cli_cmp) -> Typer:
        self._typer = cli_cmp

    def get_injector(self):
        return self._injector

    def get_settings(self):
        self.check_is_set()
        return self._settings

    def set_settings(self, some_settings: GriffSettings):
        self._settings = some_settings

    def add_component(self, a_component):
        if isinstance(a_component, AsyncRunnableComponent):
            self._async_components.append(a_component)
        self._components.append(a_component)

    def create(self):
        self._is_finalized = True
        injectable_components = [
            injectable
            for injectable in self._components
            if issubclass(type(injectable), Module)
        ]
        self._injector = Injector(injectable_components)
        self._app = self._injector.get(FastAPI)
        return self

    def replace_runtime_injectable(self, a_component: RuntimeInjectable):
        for component in self._components:
            if type(component) is not RuntimeInjectable:
                continue
            if component.get_service_type() == a_component.get_service_type():
                self._components.remove(component)
                self._components.append(a_component)
                return self

        self._components.append(a_component)
