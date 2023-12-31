from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from starlette.responses import Response
from account.services import *
from account.utils import check_auth
from fastapi import HTTPException

router = APIRouter()


@router.post('/SignUp', status_code=201, response_model=UserRegisterResponseSuccess)
async def create_user(payload: UserAuthForm):
    successful_registration = await payload.sign_up()

    if successful_registration:
        return successful_registration

    raise HTTPException(status_code=400, detail='Логин уже занят')


@router.post('/SignIn')
async def login(payload: UserAuthForm, response: Response, authorize: AuthJWT = Depends()):
    user = await payload.get_user_by_username()

    if user:
        access_token, refresh_token = await utils.set_cookie_data(response, authorize, user_id=user.id)
        return LoginSuccessSchema(status=200, access_token=access_token)

    raise HTTPException(status_code=400, detail='Неверный логин или пароль')


@router.post('/SignOut', status_code=200)
async def logout(response: Response, authorize: check_auth = Depends()):
    authorize.unset_jwt_cookies()
    response.set_cookie('logged_in', '', -1)
    return {'status': 'success'}


@router.get('/Me', response_model=UserMeInfo)
async def get_me(authorize: check_auth = Depends()):
    authorize.jwt_required()
    user_id = authorize.get_jwt_subject()
    user_info = await UserMeInfo.get_user_info(int(user_id))
    return user_info
