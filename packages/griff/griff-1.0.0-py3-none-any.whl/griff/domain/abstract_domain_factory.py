from abc import ABC, abstractmethod
from typing import Any


class AbstractDomainFactory(ABC):
    @abstractmethod
    def build_field(
        self,
        primitive_value,
        field_type: type,
        services: list = None,
        constraints: list = None,
    ) -> Any:
        # pragma: no cover
        raise NotImplementedError

    @abstractmethod
    def hydrate_field(
        self,
        primitive_value,
        field_type: type,
        services: list = None,
        constraints: list = None,
    ) -> Any:
        # pragma: no cover
        raise NotImplementedError
