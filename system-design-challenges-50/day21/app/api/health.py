from fastapi import APIRouter, Response
from datetime import datetime
import logging

router = APIRouter()

# Set up logging
logger = logging.getLogger(__name__)


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    logger.info("Health check requested")
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "social-media-api"
    }


@router.get("/ready")
async def readiness_check():
    """Readiness check endpoint"""
    logger.info("Readiness check requested")
    # In a real implementation, this would check database connectivity,
    # cache availability, and other dependencies
    return {
        "status": "ready",
        "timestamp": datetime.utcnow().isoformat(),
        "dependencies": {
            "database": "ok",
            "cache": "ok",
            "media_service": "ok"
        }
    }