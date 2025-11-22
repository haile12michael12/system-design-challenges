from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, List
import logging

from app.api.deps import get_current_user
from app.schemas.recommendation import SimulationRequest, SimulationResponse
from app.services.simulation_engine import SimulationEngineService

router = APIRouter()

# Set up logging
logger = logging.getLogger(__name__)


@router.post("/simulate", response_model=SimulationResponse)
async def run_simulation(
    request: SimulationRequest,
    current_user: dict = Depends(get_current_user)
):
    """Run a cost optimization simulation"""
    try:
        logger.info(f"Running simulation for service {request.service_id}")
        
        # Initialize service
        simulation_engine = SimulationEngineService()
        
        # Run simulation
        results = await simulation_engine.run_simulation(
            request.service_id,
            request.scenarios,
            request.duration_hours
        )
        
        return SimulationResponse(
            service_id=request.service_id,
            scenarios=results,
            generated_at="2025-11-22T00:00:00Z"
        )
    except Exception as e:
        logger.error(f"Error running simulation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to run simulation"
        )


@router.get("/simulate/templates", response_model=List[str])
async def get_simulation_templates(
    current_user: dict = Depends(get_current_user)
):
    """Get available simulation templates"""
    try:
        logger.info("Fetching simulation templates")
        
        # Initialize service
        simulation_engine = SimulationEngineService()
        
        # Get templates
        templates = await simulation_engine.get_templates()
        
        return templates
    except Exception as e:
        logger.error(f"Error fetching templates: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch templates"
        )


@router.post("/simulate/batch")
async def run_batch_simulation(
    requests: List[SimulationRequest],
    current_user: dict = Depends(get_current_user)
):
    """Run multiple simulations in batch"""
    try:
        logger.info(f"Running batch simulation for {len(requests)} requests")
        
        # Initialize service
        simulation_engine = SimulationEngineService()
        
        # Run batch simulations
        results = []
        for req in requests:
            result = await simulation_engine.run_simulation(
                req.service_id,
                req.scenarios,
                req.duration_hours
            )
            results.append(result)
        
        return {
            "status": "success",
            "results": results
        }
    except Exception as e:
        logger.error(f"Error running batch simulation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to run batch simulation"
        )