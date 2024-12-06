from abc import ABC, abstractmethod
from typing import Any, Optional

from griff.infrastructure.bus.command.command_context import CQContext


class AbstractMiddleware(ABC):
    def __init__(self):
        self._next: Optional[AbstractMiddleware] = None

    def set_next(self, middleware: "AbstractMiddleware") -> "AbstractMiddleware":
        self._next = middleware
        return middleware

    @abstractmethod
    async def dispatch(self, command: Any, context: CQContext = None) -> Any:
        if self._next:
            return self._next.dispatch(command, context)
        return None
