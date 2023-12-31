import datetime
from fastapi import Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import MissingTokenError
from starlette.responses import Response
from account.oauth import ACCESS_TOKEN_EXPIRES_IN, REFRESH_TOKEN_EXPIRES_IN
from account import db_query
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_tokens(authorize: AuthJWT, user_id: int):
    access_token = authorize.create_access_token(
        subject=str(user_id), expires_time=datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))

    refresh_token = authorize.create_refresh_token(
        subject=str(user_id), expires_time=datetime.timedelta(minutes=REFRESH_TOKEN_EXPIRES_IN))
    return access_token, refresh_token


async def set_cookie_data(response: Response, authorize: AuthJWT, user_id: int):
    access_token, refresh_token = create_tokens(authorize, user_id)

    response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('refresh_token', refresh_token,
                        REFRESH_TOKEN_EXPIRES_IN * 60, REFRESH_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')

    await db_query.update_tokens(user_id, access_token, refresh_token)
    return access_token, refresh_token


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def check_auth(authorize: AuthJWT = Depends()):
    try:
        authorize.jwt_required()
        return authorize
    except MissingTokenError:
        raise HTTPException(status_code=403, detail='Вы не авторизованы')
