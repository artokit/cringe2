from sqlalchemy import update, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from database.connect import create_session
from database.models import payments


@create_session
async def create_payment(session: AsyncSession, payment_uuid: str, payment_status: str, user_id: int, amount: float):
    q = insert(payments).values(uuid=payment_uuid, status=payment_status, user_id=user_id, amount=amount)
    await session.execute(q)
    await session.commit()


@create_session
async def get_payment(session: AsyncSession, payment_uuid: str):
    q = select(payments).where(payments.c.uuid == payment_uuid)
    return (await session.execute(q)).fetchone()


@create_session
async def edit_payment_status(session: AsyncSession, payment_uuid: str, status: str):
    q = update(payments).where(payments.c.uuid == payment_uuid).values(status=status)
    await session.execute(q)
    await session.commit()
