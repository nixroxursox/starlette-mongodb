from typing import Any, Dict, Optional, Sequence, Type
from starlette.status import HTTP_401_UNAUTHORIZED
from pydantic import BaseModel, ValidationError, create_model
from pydantic.error_wrappers import ErrorList
from starlette.middleware.exceptions import HTTPException as StarletteHTTPException


class HTTPException(StarletteHTTPException):
    """
    Docstring: This is the HTTPException from starlette.
    """
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail)
        self.headers = headers


RequestErrorModel: Type[BaseModel] = create_model("Request")
WebSocketErrorModel: Type[BaseModel] = create_model("WebSocket")


class RequestValidationError(ValidationError):
    """
    Docstring: This is the request Validation Error.
    """
    def __init__(self, errors: Sequence[ErrorList], *, body: Any = None) -> None:
        self.body = body
        super().__init__(errors, RequestErrorModel)


class WebSocketRequestValidationError(ValidationError):
    """
    Docstring: This is the WebSocket Request Validation Error.
    """

    def __init__(self, errors: Sequence[ErrorList]) -> None:
        super().__init__(errors, WebSocketErrorModel)


InvalidCredentialsException = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED,
    detail="Invalid credentials",
    headers={"WWW-Authenticate": "Bearer"}
)
