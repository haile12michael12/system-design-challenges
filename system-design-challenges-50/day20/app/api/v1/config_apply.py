from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
import logging

from app.api.deps import get_current_user
from app.schemas.recommendation import RecommendationApplyRequest
from app.services.cost_model import CostModelService

router = APIRouter()

# Set up logging
logger = logging.getLogger(__name__)


@router.post("/config/apply")
async def apply_recommendation(
    request: RecommendationApplyRequest,
    current_user: dict = Depends(get_current_user)
):
    """Apply a cost optimization recommendation"""
    try:
        logger.info(f"Applying recommendation {request.recommendation_id} for service {request.service_id}")
        
        # Initialize service
        cost_model = CostModelService()
        
        # Apply recommendation
        result = await cost_model.apply_recommendation(
            request.service_id,
            request.recommendation_id,
            request.parameters
        )
        
        return {
            "status": "success",
            "message": "Recommendation applied successfully",
            "result": result
        }
    except Exception as e:
        logger.error(f"Error applying recommendation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to apply recommendation"
        )


@router.post("/config/rollback/{service_id}/{recommendation_id}")
async def rollback_recommendation(
    service_id: str,
    recommendation_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Rollback a previously applied recommendation"""
    try:
        logger.info(f"Rolling back recommendation {recommendation_id} for service {service_id}")
        
        # Initialize service
        cost_model = CostModelService()
        
        # Rollback recommendation
        result = await cost_model.rollback_recommendation(
            service_id,
            recommendation_id
        )
        
        return {
            "status": "success",
            "message": "Recommendation rolled back successfully",
            "result": result
        }
    except Exception as e:
        logger.error(f"Error rolling back recommendation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to rollback recommendation"
        )


@router.get("/config/history/{service_id}")
async def get_config_history(
    service_id: str,
    limit: int = 10,
    current_user: dict = Depends(get_current_user)
):
    """Get configuration change history for a service"""
    try:
        logger.info(f"Fetching config history for service {service_id}")
        
        # Initialize service
        cost_model = CostModelService()
        
        # Get history
        history = await cost_model.get_config_history(
            service_id,
            limit
        )
        
        return {
            "service_id": service_id,
            "history": history
        }
    except Exception as e:
        logger.error(f"Error fetching config history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch config history"
        )