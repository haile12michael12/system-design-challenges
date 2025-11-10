"""
SQLAlchemy Engine + Session Setup
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import sessionmaker
import os

# Database URL from environment or default to SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./app.db")

# Async engine for async operations
async_engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True
)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False
)

# Sync engine for Alembic migrations
sync_engine = create_engine(
    DATABASE_URL.replace("sqlite+aiosqlite://", "sqlite://"),
    echo=True,
    future=True
)

# Sync session factory for Alembic
SyncSessionLocal = sessionmaker(
    bind=sync_engine,
    expire_on_commit=False
)

# Create async session
async def get_db():
    """Dependency for FastAPI to get DB session"""
    async with AsyncSessionLocal() as session:
        yield session