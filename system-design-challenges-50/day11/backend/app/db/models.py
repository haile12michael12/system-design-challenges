from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class HealthResponse(BaseModel):
    status: str
    service: str
    timestamp: Optional[datetime] = None

class SimulationRequest(BaseModel):
    instances: int
    workload: int
    scaling_type: str  # "vertical" or "horizontal"

class SimulationResponse(BaseModel):
    simulation_id: str
    status: str
    results: Optional[dict] = None

class MetricsData(BaseModel):
    timestamp: datetime
    latency: float
    cost: float
    instances: int

class ScalingDecision(BaseModel):
    timestamp: datetime
    action: str  # "scale_up", "scale_down", "scale_out", "scale_in"
    reason: str
    current_instances: int
    new_instances: int