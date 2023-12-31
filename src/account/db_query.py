from typing import Optional
from sqlalchemy import insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import users
from database.connect import create_session


@create_session
async def add_user(session: AsyncSession, username: str, hashed_password: str) -> bool:
    query = insert(users).values(
        username=username,
        hashed_password=hashed_password,
    )

    try:
        await session.execute(query)
        await session.commit()
        return True

    except IntegrityError:
        return False


@create_session
async def update_tokens(session: AsyncSession, user_id: int, access_token: str, refresh_token: str):
    q = update(users).where(users.c.id == user_id).values(access_token=access_token, refresh_token=refresh_token)
    await session.execute(q)
    await session.commit()
    await session.close()


@create_session
async def get_user_by_username(session: AsyncSession, username: str) -> Optional[tuple]:
    query = select(users).where(users.c.username == username)
    res = (await session.execute(query)).fetchone()
    return res


@create_session
async def get_user_by_id(session: AsyncSession, user_id: int) -> Optional[tuple]:
    q = select(users).where(users.c.id == user_id)
    res = (await session.execute(q)).fetchone()
    return res


@create_session
async def edit_balance(session: AsyncSession, id: int, balance: float):
    q = update(users).where(users.c.id == id).values(balance=balance)
    await session.execute(q)
    await session.commit()
