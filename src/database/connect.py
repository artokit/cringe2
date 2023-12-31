from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker


DATABASE_URL = f"postgresql+asyncpg://admin:admin@localhost:5432/production"
Base = declarative_base()


engine = create_async_engine(DATABASE_URL)


def create_session(f):
    async def wrapper(*args, **kwargs):
        session = await get_async_session()
        res = await f(session, *args, **kwargs)
        await session.close()
        return res
    return wrapper


async def get_async_session() -> AsyncSession:
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as s:
        return s
