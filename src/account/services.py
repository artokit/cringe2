import datetime
from dataclasses import dataclass
from typing import Optional
from pydantic import BaseModel
from account import utils, db_query


@dataclass
class User:
    id: int
    username: str
    hashed_password: str
    admin: bool
    access_token: str
    refresh_token: str
    balance: float

    @staticmethod
    async def edit_balance(user_id: int, balance: float):
        await db_query.edit_balance(user_id, balance)


class UserRegisterResponseSuccess(BaseModel):
    time_register_user: datetime.datetime


class LoginSuccessSchema(BaseModel):
    status: int
    access_token: str


class UserAuthForm(BaseModel):
    username: str
    password: str

    async def sign_up(self) -> Optional[UserRegisterResponseSuccess]:
        self.password = utils.get_password_hash(self.password)
        success = await db_query.add_user(self.username, self.password)

        if success:
            return UserRegisterResponseSuccess(time_register_user=datetime.datetime.now())

    async def get_user_by_username(self) -> Optional[User]:
        user = await db_query.get_user_by_username(self.username)

        if user and utils.verify_password(self.password, user[2]):
            return User(*user)


class UserMeInfo(BaseModel):
    id: int
    username: str
    is_admin: bool
    balance: float

    @staticmethod
    async def get_user_info(user_id: int):
        user = await db_query.get_user_by_id(user_id)
        return UserMeInfo(id=user[0], username=user[1], is_admin=user[3], balance=user[6])
