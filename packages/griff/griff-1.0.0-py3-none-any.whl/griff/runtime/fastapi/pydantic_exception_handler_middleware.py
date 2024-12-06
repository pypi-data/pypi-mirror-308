from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from pydantic_i18n import PydanticI18n
from starlette.responses import JSONResponse

from griff.runtime.fastapi.validation_exception_simplifier import simplify_errors


class PydanticValidationExceptionHandlerMiddleware:
    def __init__(self, pydantic_i18n: PydanticI18n) -> None:
        self._i18n = pydantic_i18n

    async def dispatch(
        self, request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        current_locale = request.query_params.get("locale", self._i18n.default_locale)
        errors = self._i18n.translate(exc.errors(), current_locale)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "msg": "validation error",
                "opcode": "422",
                "details": simplify_errors(errors),
            },
        )
