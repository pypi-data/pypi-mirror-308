from griff.infrastructure.bus.command.abstract_command import AbstractCommandResponse
from griff.infrastructure.bus.middlewares.abstract_middleware import AbstractMiddleware


class SuccessCommandResponse(AbstractCommandResponse):
    ...


class FakeExceptionMiddleware(AbstractMiddleware):
    async def dispatch(self, command, context=None) -> AbstractCommandResponse:
        raise SystemError(
            "Exception de test pour vérifier le rollback de l'unit of work"
        )


class FakeResponseMiddleware(AbstractMiddleware):
    async def dispatch(self, command, context=None) -> AbstractCommandResponse:
        return SuccessCommandResponse(code=200, msg="Success")
