"""
Health Check Endpoint
"""
from fastapi import APIRouter, Response
from pydantic import BaseModel

router = APIRouter()

class HealthResponse(BaseModel):
    status: str = "healthy"
    service: str = "instagram-feed"

@router.get("/", response_model=HealthResponse)
async def health_check():
    return HealthResponse()