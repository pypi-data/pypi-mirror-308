from abc import ABC, abstractmethod
from inspect import getmembers
from types import FunctionType
from typing import Any, Iterator

from typer import Typer


class AbstractCliController(ABC):
    def __init__(self):
        self._app = self._build_app()

    def get_app(self):
        return self._app

    @abstractmethod
    def get_command_name(self) -> str:
        raise NotImplementedError

    def _build_app(self) -> Typer:
        app = Typer()
        self._register_endpoints(app)
        return app

    def _register_endpoints(self, app: Typer):
        cls = type(self)

        for endpoint in cls._get_endpoints():
            name = getattr(endpoint, "_endpoint_name")
            method = endpoint.__get__(self, cls)
            app.command(name)(method)

    @classmethod
    def _get_endpoints(cls) -> Iterator[FunctionType]:
        def is_endpoint(member: Any) -> bool:
            return isinstance(member, FunctionType) and hasattr(
                member, "_endpoint_name"
            )

        return (value for _, value in getmembers(cls, is_endpoint))
