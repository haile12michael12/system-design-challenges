from fastapi import APIRouter, Depends
from typing import Dict, Any

from ..core.monitoring import REQUEST_COUNT, REQUEST_DURATION

router = APIRouter(prefix="/debug", tags=["debug"])


@router.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint.
    
    Returns:
        Dict[str, str]: Health status
    """
    return {"status": "healthy", "service": "feed-service"}


@router.get("/metrics-summary")
async def metrics_summary() -> Dict[str, Any]:
    """
    Get a summary of Prometheus metrics.
    
    Returns:
        Dict[str, Any]: Metrics summary
    """
    # Get metrics data
    request_count_metrics = {}
    for sample in REQUEST_COUNT.collect()[0].samples:
        labels = sample.labels
        key = f"{labels['method']}_{labels['endpoint']}_{labels['status']}"
        request_count_metrics[key] = sample.value
    
    duration_metrics = {}
    for sample in REQUEST_DURATION.collect()[0].samples:
        labels = sample.labels
        key = f"{labels['method']}_{labels['endpoint']}"
        duration_metrics[key] = sample.value
    
    return {
        "request_counts": request_count_metrics,
        "request_durations": duration_metrics
    }


@router.get("/config")
async def get_config() -> Dict[str, Any]:
    """
    Get current configuration.
    
    Returns:
        Dict[str, Any]: Current configuration
    """
    from ..core.config import settings
    
    return {
        "database_url": settings.DATABASE_URL,
        "redis_url": settings.REDIS_URL,
        "debug": settings.DEBUG,
        "environment": settings.ENVIRONMENT
    }