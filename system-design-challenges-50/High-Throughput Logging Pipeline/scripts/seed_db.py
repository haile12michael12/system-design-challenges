#!/usr/bin/env python3
"""
Seed the database with initial data for testing
"""
import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))

from app.db.base import engine, Base
from app.db.models import LogEntry, Tenant

async def seed_database():
    """
    Seed the database with initial data
    """
    print("Seeding database...")
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    print("Database seeded successfully!")

if __name__ == "__main__":
    asyncio.run(seed_database())