from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import asyncio

class CAPConfiguration(BaseModel):
    consistency_level: str  # "strong", "eventual", "causal"
    availability_level: str  # "high", "medium", "low"
    partition_tolerance: bool  # True/False

class CAPSimulationRequest(BaseModel):
    config: CAPConfiguration
    duration_seconds: int = 30

class CAPState(BaseModel):
    timestamp: datetime
    consistency: float  # 0.0 to 1.0
    availability: float  # 0.0 to 1.0
    partition_status: bool  # True if partition exists
    latency: float  # in milliseconds

class CAPSimulationResponse(BaseModel):
    simulation_id: str
    status: str  # "running", "completed", "failed"
    states: List[CAPState] = []
    final_consistency: float
    final_availability: float

router = APIRouter()

# In-memory storage for simulations (in production, use Redis or database)
simulations = {}

@router.post("/cap/simulate", response_model=CAPSimulationResponse)
async def start_cap_simulation(request: CAPSimulationRequest, background_tasks: BackgroundTasks):
    """Start a new CAP theorem simulation"""
    import uuid
    simulation_id = str(uuid.uuid4())
    
    # Initialize simulation
    simulations[simulation_id] = {
        "status": "running",
        "states": [],
        "config": request.config
    }
    
    # Run simulation in background
    background_tasks.add_task(run_cap_simulation, simulation_id, request)
    
    return CAPSimulationResponse(
        simulation_id=simulation_id,
        status="running",
        final_consistency=0.0,
        final_availability=0.0
    )

@router.get("/cap/simulation/{simulation_id}", response_model=CAPSimulationResponse)
async def get_simulation_status(simulation_id: str):
    """Get the status of a CAP simulation"""
    if simulation_id not in simulations:
        return CAPSimulationResponse(
            simulation_id=simulation_id,
            status="not_found",
            final_consistency=0.0,
            final_availability=0.0
        )
    
    sim = simulations[simulation_id]
    states = sim.get("states", [])
    
    # Calculate final values
    final_consistency = states[-1].consistency if states else 0.0
    final_availability = states[-1].availability if states else 0.0
    
    return CAPSimulationResponse(
        simulation_id=simulation_id,
        status=sim["status"],
        states=states,
        final_consistency=final_consistency,
        final_availability=final_availability
    )

async def run_cap_simulation(simulation_id: str, request: CAPSimulationRequest):
    """Run the CAP theorem simulation in the background"""
    try:
        duration = request.duration_seconds
        config = request.config
        
        # Simulate for the specified duration
        for i in range(duration):
            # Simulate CAP state changes
            consistency = calculate_consistency(config, i)
            availability = calculate_availability(config, i)
            partition_status = simulate_partition(config, i)
            latency = calculate_latency(config, i)
            
            state = CAPState(
                timestamp=datetime.now(),
                consistency=consistency,
                availability=availability,
                partition_status=partition_status,
                latency=latency
            )
            
            # Store state
            simulations[simulation_id]["states"].append(state)
            
            # Wait 1 second between updates
            await asyncio.sleep(1)
        
        # Mark simulation as completed
        simulations[simulation_id]["status"] = "completed"
        
    except Exception as e:
        # Mark simulation as failed
        simulations[simulation_id]["status"] = "failed"
        print(f"Simulation failed: {e}")

def calculate_consistency(config: CAPConfiguration, time_step: int) -> float:
    """Calculate consistency based on configuration and time"""
    base_consistency = 0.8 if config.consistency_level == "strong" else 0.5 if config.consistency_level == "causal" else 0.3
    
    # Simulate fluctuations
    import random
    fluctuation = random.uniform(-0.1, 0.1)
    
    # If partition exists, consistency drops
    if config.partition_tolerance and time_step > 10:
        fluctuation -= 0.3
    
    return max(0.0, min(1.0, base_consistency + fluctuation))

def calculate_availability(config: CAPConfiguration, time_step: int) -> float:
    """Calculate availability based on configuration and time"""
    base_availability = 0.9 if config.availability_level == "high" else 0.7 if config.availability_level == "medium" else 0.5
    
    # Simulate fluctuations
    import random
    fluctuation = random.uniform(-0.1, 0.1)
    
    # If partition exists, availability might be affected
    if config.partition_tolerance and time_step > 10:
        fluctuation -= 0.2
    
    return max(0.0, min(1.0, base_availability + fluctuation))

def simulate_partition(config: CAPConfiguration, time_step: int) -> bool:
    """Simulate network partition status"""
    # Partitions occur after 10 seconds in simulations with partition tolerance
    return config.partition_tolerance and time_step > 10

def calculate_latency(config: CAPConfiguration, time_step: int) -> float:
    """Calculate latency based on configuration and time"""
    base_latency = 50.0 if config.consistency_level == "strong" else 30.0 if config.consistency_level == "causal" else 20.0
    
    # If partition exists, latency increases
    if config.partition_tolerance and time_step > 10:
        base_latency += 100.0
    
    # Add some random variation
    import random
    variation = random.uniform(-10.0, 10.0)
    
    return max(0.0, base_latency + variation)