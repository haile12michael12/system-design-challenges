from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
import logging

from app.api.deps import get_current_user
from app.schemas.recommendation import RecommendationRequest, RecommendationResponse
from app.services.cost_model import CostModelService
from app.services.sla_engine import SLAEngineService

router = APIRouter()

# Set up logging
logger = logging.getLogger(__name__)


@router.post("/recommend", response_model=RecommendationResponse)
async def get_recommendations(
    request: RecommendationRequest,
    current_user: dict = Depends(get_current_user)
):
    """Get cost optimization recommendations"""
    try:
        logger.info(f"Generating recommendations for user {current_user.get('user_id')}")
        
        # Initialize services
        cost_model = CostModelService()
        sla_engine = SLAEngineService()
        
        # Get current resource usage
        current_usage = await cost_model.get_current_usage(request.service_id)
        
        # Generate recommendations
        recommendations = await cost_model.generate_recommendations(
            request.service_id,
            current_usage,
            request.budget_constraints
        )
        
        # Validate SLA compliance
        validated_recommendations = await sla_engine.validate_recommendations(
            request.service_id,
            recommendations
        )
        
        return RecommendationResponse(
            recommendations=validated_recommendations,
            generated_at=validated_recommendations[0].generated_at if validated_recommendations else None
        )
    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate recommendations"
        )


@router.get("/recommendations/{service_id}", response_model=List[RecommendationResponse])
async def get_service_recommendations(
    service_id: str,
    limit: int = 10,
    current_user: dict = Depends(get_current_user)
):
    """Get historical recommendations for a service"""
    try:
        logger.info(f"Fetching historical recommendations for service {service_id}")
        
        # Initialize services
        cost_model = CostModelService()
        
        # Get historical recommendations
        recommendations = await cost_model.get_historical_recommendations(
            service_id,
            limit
        )
        
        return recommendations
    except Exception as e:
        logger.error(f"Error fetching historical recommendations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch historical recommendations"
        )