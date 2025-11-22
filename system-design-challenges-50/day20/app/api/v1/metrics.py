from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any
import logging

from app.api.deps import get_current_user
from app.schemas.metrics import MetricsRequest, MetricsResponse
from app.services.telemetry_connector import TelemetryConnectorService

router = APIRouter()

# Set up logging
logger = logging.getLogger(__name__)


@router.post("/metrics/query", response_model=MetricsResponse)
async def query_metrics(
    request: MetricsRequest,
    current_user: dict = Depends(get_current_user)
):
    """Query service metrics"""
    try:
        logger.info(f"Querying metrics for service {request.service_id}")
        
        # Initialize service
        telemetry_service = TelemetryConnectorService()
        
        # Query metrics
        metrics_data = await telemetry_service.query_metrics(
            request.service_id,
            request.metric_names,
            request.start_time,
            request.end_time,
            request.aggregation
        )
        
        return MetricsResponse(
            service_id=request.service_id,
            metrics=metrics_data,
            query_time=request.start_time
        )
    except Exception as e:
        logger.error(f"Error querying metrics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to query metrics"
        )


@router.get("/metrics/services", response_model=List[str])
async def list_monitored_services(
    current_user: dict = Depends(get_current_user)
):
    """List all monitored services"""
    try:
        logger.info("Listing monitored services")
        
        # Initialize service
        telemetry_service = TelemetryConnectorService()
        
        # Get service list
        services = await telemetry_service.list_services()
        
        return services
    except Exception as e:
        logger.error(f"Error listing services: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list services"
        )


@router.get("/metrics/{service_id}/health")
async def get_service_health(
    service_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get health status for a service"""
    try:
        logger.info(f"Checking health for service {service_id}")
        
        # Initialize service
        telemetry_service = TelemetryConnectorService()
        
        # Get health status
        health_status = await telemetry_service.get_service_health(service_id)
        
        return {
            "service_id": service_id,
            "status": health_status,
            "timestamp": "2025-11-22T00:00:00Z"
        }
    except Exception as e:
        logger.error(f"Error checking service health: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to check service health"
        )