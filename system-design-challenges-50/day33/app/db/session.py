"""
Database Session Management
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Async engine for async operations
async_engine = create_async_engine(
    settings.DATABASE_URL.replace("sqlite://", "sqlite+aiosqlite://"),
    echo=True,
    future=True
)

# Sync engine for Alembic migrations
sync_engine = create_engine(
    settings.DATABASE_URL,
    echo=True,
    future=True
)

# Session factories
AsyncSessionLocal = async_sessionmaker(bind=async_engine, expire_on_commit=False)
SyncSessionLocal = sessionmaker(bind=sync_engine, expire_on_commit=False)

# Create async session
async def get_db():
    """Dependency for FastAPI to get DB session"""
    async with AsyncSessionLocal() as session:
        yield session