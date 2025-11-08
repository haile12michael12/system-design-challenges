from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from app.db.base import engine
from typing import AsyncGenerator

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get an async database session"""
    session = async_sessionmaker(engine, expire_on_commit=False)
    async with session() as async_session:
        yield async_session