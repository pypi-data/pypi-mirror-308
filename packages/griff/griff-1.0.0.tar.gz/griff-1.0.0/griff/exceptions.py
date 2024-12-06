from typing import Optional

from griff.opcode import WBaseOpCode


class WError(Exception):
    """
    Base class for exceptions

    Attributes:
        message (str): Error message
        code (int): code like HTTP status code
    """

    status_code = 500
    message: str = "error message"
    operational_code: WBaseOpCode = WBaseOpCode.DEFAULT_OPCODE_ERROR

    def __init__(self, message: str = None, details: dict = None) -> None:
        if message:
            self.message = message
        self.code = self.status_code
        self.details = details or None

    def __str__(self) -> str:
        return f"{self.code} - {self.message} - {self.details}"

    def get_message(self):
        return self.message

    def get_code(self):
        return self.code

    def get_opcode(self):
        return self.operational_code.value

    def get_details(self):
        return self.details

    def to_dict(self) -> dict:
        a_dict = {"msg": self.get_message(), "opcode": str(self.get_opcode())}
        if self.details is not None:
            a_dict["details"] = self.details
        return a_dict


class NotFoundError(WError):
    """Raised when something is not found"""

    status_code = 404

    def __init__(self, message, params=None) -> None:
        super().__init__(message, params)


class AlreadyExistsError(WError):
    """Raised when something already exists"""

    status_code = 409
    message = "Entity or Aggregate already exists"
    detail = None

    def __init__(self, detail=None, params=None) -> None:
        super().__init__(self.message, params)
        self.detail = detail


class ValidationError(WError):
    """Raised when data validation failed"""

    status_code = 422
    message = "Unprocessable Entity"
    detail = None

    def __init__(self, detail=None, params=None) -> None:
        super().__init__(self.message, params)
        self.detail = detail


class AuthenticationTimeoutError(WError):
    """Raise when Authentification Timeout"""

    status_code = 403
    message = "Authentication Timeout"

    def __init__(self, message=None, params=None) -> None:
        super().__init__(message, params)


class AccessForbiddenError(WError):
    """Raise when access is forbidden"""

    status_code = 403
    message = "Unsufficient permission level, Access Forbidden"
    operational_code = WBaseOpCode.ACCESS_FORBIDDEN_ERROR

    def __init__(self, message=None, params=None) -> None:
        super().__init__(message, params)


class BadRequestError(WError):
    """
    Raise on an apparent client (e.g., malformed request syntax, size too large, ...)
    """

    status_code = 400
    message = "Bad Request"


class ServiceUnavailable(WError):
    status_code = 503
    message = "Service temporarily unavailable, try again later."


class CommandException(WError):
    def __init__(
        self, message: Optional[str] = None, code: Optional[int] = None, errors=None
    ) -> None:
        super().__init__(message, code)
        self.errors = errors

    def __str__(self):
        return f"CommandException<code={self.code}>"


class EntityNotFoundError(WError):
    status_code = 404
    message = "entity not found"
