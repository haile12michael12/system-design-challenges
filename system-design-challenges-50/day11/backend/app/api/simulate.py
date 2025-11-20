from fastapi import APIRouter, BackgroundTasks
from ..db.models import SimulationRequest, SimulationResponse
from ..services.simulator import run_simulation
import uuid

router = APIRouter()

@router.post("/simulate", response_model=SimulationResponse)
async def start_simulation(request: SimulationRequest, background_tasks: BackgroundTasks):
    """Start a new simulation"""
    simulation_id = str(uuid.uuid4())
    
    # Run simulation in background
    background_tasks.add_task(run_simulation, simulation_id, request)
    
    return SimulationResponse(
        simulation_id=simulation_id,
        status="started"
    )

@router.get("/simulate/{simulation_id}", response_model=SimulationResponse)
async def get_simulation(simulation_id: str):
    """Get simulation results"""
    # In a real implementation, this would fetch from a database
    # For now, we'll return a mock response
    return SimulationResponse(
        simulation_id=simulation_id,
        status="completed",
        results={
            "latency_data": [],
            "cost_data": [],
            "scaling_decisions": []
        }
    )