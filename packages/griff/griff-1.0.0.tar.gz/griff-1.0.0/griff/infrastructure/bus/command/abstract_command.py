from abc import ABC, abstractmethod
from dataclasses import field
from typing import Any, List, Type

from injector import inject
from pydantic import BaseModel

from griff.domain.auto_vo.user_permission_vo import UserPermissionType
from griff.infrastructure.bus.command.command_context import CQContext
from griff.infrastructure.bus.event.abstract_event import AbstractDomainEvent
from griff.infrastructure.bus.middlewares.abstract_middleware import AbstractMiddleware
from griff.infrastructure.registry.meta_registry import MetaCommandHandlerRegistry
from griff.services.uuid.uuid_service import UuidService


class PermissionMixin(BaseModel):
    required_permission: UserPermissionType = UserPermissionType.SUPER_ADMIN


class AbstractCommand(PermissionMixin, ABC):
    @abstractmethod
    def to_history(self) -> dict[str, Any]:
        return self.model_dump()

    @classmethod
    def get_name(cls) -> str:
        return cls.__name__

    @classmethod
    def get_type(cls) -> str:
        return "COMMAND"


class AbstractCommandResponse(BaseModel, ABC):
    code: int
    msg: str = None
    errors: dict = None
    linked_events: List[AbstractDomainEvent] = field(default_factory=list)
    details: dict = None

    def has_events(self):
        if self.events is not None and len(self.linked_events) > 0:
            return True
        return False

    def events(self):
        return self.linked_events


class AbstractCommandHandler(ABC, metaclass=MetaCommandHandlerRegistry):
    @inject
    def __init__(self, uuid_service: UuidService = UuidService()):
        self._uuid_service = uuid_service

    @abstractmethod
    async def handle(
        self, command: AbstractCommand, context: CQContext = None
    ) -> AbstractCommandResponse:
        pass

    @classmethod
    @abstractmethod
    def listen_to(cls) -> Type:
        pass


class AbstractCommandMiddleware(AbstractMiddleware, ABC):
    def __init__(self):
        super().__init__()
        self._next: AbstractCommandMiddleware

    @abstractmethod
    async def dispatch(
        self, command: AbstractCommand, context: CQContext = None
    ) -> AbstractCommandResponse:
        ...
