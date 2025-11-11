"""
Dashboard Route
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any

router = APIRouter()

class MetricsResponse(BaseModel):
    cpu_usage: float
    memory_usage: float
    replicas: int
    cost_per_hour: float

class AutoscalerStatus(BaseModel):
    enabled: bool
    target_cpu: float
    min_replicas: int
    max_replicas: int

@router.get("/metrics", response_model=MetricsResponse)
async def get_metrics():
    """Get current metrics"""
    return MetricsResponse(
        cpu_usage=50.0,
        memory_usage=60.0,
        replicas=3,
        cost_per_hour=0.15
    )

@router.get("/status", response_model=AutoscalerStatus)
async def get_status():
    """Get autoscaler status"""
    return AutoscalerStatus(
        enabled=True,
        target_cpu=70.0,
        min_replicas=1,
        max_replicas=10
    )

@router.post("/scale")
async def trigger_scaling():
    """Trigger manual scaling"""
    return {"message": "Scaling triggered"}