from fastapi import Request
from loguru import logger
from starlette.responses import JSONResponse

from griff.exceptions import CommandException


def command_exception_handler(request: Request, exc: CommandException) -> JSONResponse:
    content = exc.errors if exc.errors else exc.message
    logger.error(f"command error: {exc}")
    logger.debug(content)
    return JSONResponse(
        status_code=exc.code,
        content=content,
    )
