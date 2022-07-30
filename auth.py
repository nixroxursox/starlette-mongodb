from pydantic import BaseModel, Field, SecretBytes, validator
from starlette.status import HTTP_401_UNAUTHORIZED
from starlette_login.decorator import login_required
from starlette_login.login_manager import LoginManager as lm
import nacl
from nacl import utils
from db import dataBase
from starlette.exceptions import HTTPException
from user import login
from starlette.authentication import (
    AuthCredentials, AuthenticationBackend, AuthenticationError, SimpleUser, BaseUser
)
from starlette_login.backends import SessionAuthBackend
from starlette_login.login_manager import LoginManager
from starlette_login.middleware import AuthenticationMiddleware
from starlette.config import Config
from starlette.requests import Request, HTTPConnection
from starlette.responses import Response
from starlette import status
config = Config(".env")

InvalidCredentialsException = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED,
    detail="Invalid credentials",
    headers={"WWW-Authenticate": "Bearer"}
)

async def authClass(AuthenticationBackend):
    async def authenticate(self, conn):
        if "Authorization" not in conn.headers:
            return InvalidCredentialsException

    auth = conn.headers["Authorization"]
    try:
        scheme, credentials = auth.split()
        if scheme.lower() != 'basic':
            return
        decoded = base64.b64decode(credentials).decode("ascii")
    except (ValueError, UnicodeDecodeError, binascii.Error) as exc:
        raise AuthenticationError('Invalid basic auth credentials')

    username, _, password = decoded.partition(":")
    # TODO: You'd want to verify the username and password here.
    return AuthCredentials(["authenticated"]), SimpleUser(username)



@login_required
async def logout_page(request: Request):
    if request.method == 'POST':
        # Logout user
        await logout_user(request)
        return RedirectResponse('/', status_code=302)

    return template.TemplateResponse(
        'logout.html', context={"request": request}
    )


@login_required
async def protected_page(request: Request):
    template = 'protected.html'
    context = {"request": request}
    headers = {
        "Authenticated": "request.user.is_authenticated"
    }
    return template.TemplateResponse(
        template,
        context,
        headers
    )


@login_required
async def admin_page(request: Request):
    # Authenticated user have `is_admin` property
    if not request.user.is_admin:
        # Not and admin user
        return RedirectResponse('/', status_code=302)
    return template.TemplateResponse(
        'admin.html', context={"request": request}
    )

async def user(request):
    username = request.path_params.get("username")

@login_required
async def protected_page(request: Request):
    return PlainTextResponse(f'You are logged in as {request.user.username}')
