from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_db
from typing import Dict

router = APIRouter()

@router.get("/")
async def health_check(db: AsyncSession = Depends(get_db)) -> Dict[str, str]:
    """Health check endpoint"""
    try:
        # Test database connection
        await db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}