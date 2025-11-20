from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class HealthResponse(BaseModel):
    status: str
    service: str
    timestamp: Optional[datetime] = None

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy", 
        service="cap-theorem-backend",
        timestamp=datetime.now()
    )