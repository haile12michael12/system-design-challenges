from fastapi import APIRouter, Depends
from typing import Dict, Any

router = APIRouter(prefix="/debug", tags=["debug"])


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "eventually-consistent-social-feed",
        "version": "1.0.0"
    }


@router.get("/metrics")
async def metrics() -> Dict[str, Any]:
    """Metrics endpoint (simplified)."""
    # In a real implementation, this would integrate with Prometheus
    return {
        "requests_processed": 100,
        "active_connections": 5,
        "cache_hits": 80,
        "cache_misses": 20
    }


@router.get("/info")
async def service_info() -> Dict[str, Any]:
    """Service information endpoint."""
    return {
        "name": "Eventually Consistent Social Feed",
        "description": "A social feed service with eventual consistency",
        "architecture": "Event-driven, microservices",
        "consistency_model": "Eventually consistent"
    }