from pydantic import BaseModel, Field, SecretBytes, validator
from starlette.status import HTTP_401_UNAUTHORIZED
from user import login
from starlette_login.login_manager import LoginManager as lm
import nacl
from nacl import utils
from db import dataBase
from starlette.exceptions import HTTPException
from user import login
from starlette.authentication import (
    AuthCredentials, AuthenticationBackend, AuthenticationError, SimpleUser, BaseUser
)
InvalidCredentialsException = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED,
    detail="Invalid credentials",
    headers={"WWW-Authenticate": "Bearer"}
)

class oauth2:
    """
    Logs in the user provided by form_data.username and form_data.password
    """
    def userGet(chkUser):
        user = dataBase.findUser(chkUser)
        if user is None:
            raise InvalidCredentialsException
        if not dataBase.chkPass(password):
            raise InvalidCredentialsException

#    token = manager.create_access_token(data={'sub': username})
#    return Token(access_token=token, token_type='bearer')


class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn):
        if "Authorization" not in conn.headers:
            return

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
