from fastapi import APIRouter
from ..db.models import HealthResponse

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint"""
    return HealthResponse(status="healthy", service="autoscaler-backend")