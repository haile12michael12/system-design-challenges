#!/usr/bin/env python3
"""
Initialize the database tables
"""
import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))

from app.db.session import engine, Base
from app.db.models import Document, DocumentVersion, DocumentOperation

async def init_db():
    """
    Create all database tables
    """
    print("Initializing database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully!")

if __name__ == "__main__":
    asyncio.run(init_db())