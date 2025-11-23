from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost:5432/failover_db")

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    """Dependency to get database session"""
    async with AsyncSessionLocal() as session:
        yield session