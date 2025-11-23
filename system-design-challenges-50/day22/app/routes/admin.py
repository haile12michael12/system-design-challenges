from fastapi import APIRouter, Depends
from app.schemas.common import SuccessResponse
from app.services.cost_optimizer import optimize_costs
from app.services.rollup_service import generate_rollups

router = APIRouter()

@router.post("/optimize-costs", response_model=SuccessResponse)
async def trigger_cost_optimization():
    """Trigger cost optimization processes"""
    optimize_costs()
    return SuccessResponse(message="Cost optimization triggered")

@router.post("/generate-rollups", response_model=SuccessResponse)
async def trigger_rollup_generation():
    """Trigger metadata rollup generation"""
    generate_rollups()
    return SuccessResponse(message="Rollup generation triggered")