from abc import ABC

from griff.infrastructure.registry.meta_registry import MetaEntryPointRegistry


class AbstractEntryPoint(ABC, metaclass=MetaEntryPointRegistry):
    def get_router(self):
        return self._router.get_router()
