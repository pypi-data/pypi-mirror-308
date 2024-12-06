from abc import ABC, abstractmethod
from typing import Any, Type

from pydantic import BaseModel

from griff.infrastructure.bus.command.command_context import CQContext
from griff.infrastructure.bus.middlewares.abstract_middleware import AbstractMiddleware
from griff.infrastructure.registry.meta_registry import MetaEventHandlerRegistry


class AbstractEvent(BaseModel, ABC):
    @abstractmethod
    def to_history(self) -> dict[str, Any]:
        return self.model_dump()

    @classmethod
    def get_name(cls) -> str:
        return cls.__name__

    @classmethod
    def get_type(cls) -> str:
        return "EVENT"


class AbstractDomainEvent(AbstractEvent, ABC):
    event_type: str
    entity_id: str
    payload: dict

    def __str__(self):
        return f"{str(self.__class__.__name__)} : {self.entity_id}"


class AbstractEventHandler(ABC, metaclass=MetaEventHandlerRegistry):
    @abstractmethod
    async def handle(self, event: AbstractEvent, context: CQContext = None) -> None:
        pass

    @classmethod
    @abstractmethod
    def listen_to(cls) -> Type:
        pass


class AbstractEventMiddleware(AbstractMiddleware, ABC):
    def __init__(self):
        super().__init__()
        self._next: AbstractEventMiddleware

    @abstractmethod
    async def dispatch(self, command: AbstractEvent, context=None) -> None:
        ...
