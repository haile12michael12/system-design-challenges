from fastapi import APIRouter, Response
from datetime import datetime

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "day19-file-storage-service"
    }


@router.get("/ready")
async def readiness_check():
    """Readiness check endpoint"""
    # In a real implementation, this would check database connectivity,
    # cache availability, and other dependencies
    return {
        "status": "ready",
        "timestamp": datetime.utcnow().isoformat(),
        "dependencies": {
            "database": "ok",
            "storage": "ok",
            "wal": "ok"
        }
    }