from fastapi import APIRouter
from ..db.models import ScalingDecision
from ..services.autoscaler import get_scaling_recommendation

router = APIRouter()

@router.get("/autoscale/recommend", response_model=ScalingDecision)
async def get_scaling_recommendation_endpoint(current_instances: int, workload: int):
    """Get autoscaling recommendation"""
    recommendation = get_scaling_recommendation(current_instances, workload)
    return recommendation