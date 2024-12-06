from fastapi import HTTPException
from starlette import status
from starlette.responses import JSONResponse

from griff.exceptions import WError
from griff.runtime.fastapi.validation_exception_simplifier import simplify_errors


class DefaultExceptionHandlerMiddleware:
    async def catch(self, request, exception_object):
        if isinstance(exception_object, WError):
            details = exception_object.details
            if exception_object.status_code == 422:
                details = simplify_errors(details or [])
            return JSONResponse(
                status_code=exception_object.status_code,
                content={
                    "msg": str(exception_object.get_message()),
                    "opcode": str(exception_object.get_opcode()),
                    "details": details,
                },
            )
        if isinstance(exception_object, HTTPException):  # pragma no cover
            return JSONResponse(
                status_code=exception_object.status_code,
                content=str(exception_object.detail),
            )
        return JSONResponse(  # pragma no cover
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=str(exception_object),
        )
