from abc import ABC
from typing import Callable

from fastapi import APIRouter

from griff.infrastructure.registry.meta_registry import MetaRouterRegistry


class AbstractRouter(ABC, metaclass=MetaRouterRegistry):
    def __init__(self):
        for ctrl in self._controllers:
            for endpoint in ctrl.get_endpoints():
                self.add_endpoint(**endpoint)

    def get_router(self) -> APIRouter:
        return self._router

    def add_endpoint(self, route: str, method: str, func: Callable, return_code: int):
        self._router.add_api_route(
            path=route, endpoint=func, methods=[method], status_code=return_code
        )
