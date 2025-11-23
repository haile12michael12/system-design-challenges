from fastapi import APIRouter, HTTPException
from app.orchestrator.lag import simulate_replication_lag
from app.orchestrator.controller import simulate_outage
from typing import Dict

router = APIRouter()

@router.post("/lag")
async def simulate_lag(region: str, delay_seconds: int = 5) -> Dict[str, str]:
    """Simulate replication lag in a specific region"""
    try:
        await simulate_replication_lag(region, delay_seconds)
        return {"status": "success", "message": f"Simulated {delay_seconds}s lag in region {region}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/outage")
async def simulate_outage_endpoint(region: str) -> Dict[str, str]:
    """Simulate an outage in a specific region"""
    try:
        await simulate_outage(region)
        return {"status": "success", "message": f"Simulated outage in region {region}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))