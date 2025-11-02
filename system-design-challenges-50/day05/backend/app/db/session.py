"""Database session management"""
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings

# Synchronous engine and session
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Asynchronous engine and session
async_engine = create_async_engine(settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"))
AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

def get_db():
    """Get synchronous database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_async_db():
    """Get asynchronous database session"""
    async with AsyncSessionLocal() as db:
        yield db