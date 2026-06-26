"""Shared structured-error model and the error codes common to all services."""

from enum import Enum

from pydantic import BaseModel


class CommonErrorCode(str, Enum):
    """Error codes shared by every HTTP service. Each service defines its own
    ``ErrorCode`` that includes these plus its service-specific codes."""

    UNAUTHORIZED = "UNAUTHORIZED"
    RATE_LIMITED = "RATE_LIMITED"
    INVALID_INPUT = "INVALID_INPUT"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    PATH_NOT_FOUND = "PATH_NOT_FOUND"
    PERMISSION_DENIED = "PERMISSION_DENIED"


class ErrorResponse(BaseModel):
    """The single structured-error shape used by every service.

    ``code`` is a plain ``str`` on the wire so any service's ``ErrorCode``
    serialises in without this package needing to know every code.
    """

    status: str
    code: str
    detail: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "error",
                "code": "UNAUTHORIZED",
                "detail": "Missing API key.",
            }
        }
    }
