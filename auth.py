from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field, SecretBytes, validator
from starlette.status import HTTP_401_UNAUTHORIZED
from user import login

InvalidCredentialsException = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED,
    detail="Invalid credentials",
    headers={"WWW-Authenticate": "Bearer"}
)



from app.models.auth import Token


def oauth2(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)) -> Token:
    """
    Logs in the user provided by form_data.username and form_data.password
    """
    user = get_user_by_name(rformsdata['username'], db)
    if user is None:
        raise InvalidCredentialsException

    if not verify_password(rformsdata['password'], password):
        raise InvalidCredentialsException

    token = manager.create_access_token(data={'sub': username})
    return Token(access_token=token, token_type='bearer')
