from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from database.connect import create_session
from database.models import transports


@create_session
async def get_car(session: AsyncSession, id: int):
    q = select(transports).where(transports.c.id == id)
    res = await session.execute(q)
    return res.fetchone()


@create_session
async def add_car(session: AsyncSession, transport, user_id: int) -> int:
    d = transport.__dict__
    d['transportType'] = transport.transportType.value
    d['owner_id'] = user_id
    del d['__pydantic_initialised__']
    q = insert(transports).values(**d)
    res = await session.execute(q)
    await session.commit()
    return res.inserted_primary_key[0]


@create_session
async def delete_car(session: AsyncSession, id: int):
    q = delete(transports).where(transports.c.id == id)
    await session.execute(q)
    await session.commit()


@create_session
async def update_car(session: AsyncSession, id: int, transport):
    d = transport.__dict__
    del d['__pydantic_initialised__']
    d['transportType'] = transport.transportType.value
    q = update(transports).where(transports.c.id == id).values(**d)
    await session.execute(q)
    await session.commit()
