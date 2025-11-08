from fastapi import APIRouter, status
from app.schemas.health import HealthResponse

router = APIRouter()

@router.get("/", response_model=HealthResponse, status_code=status.HTTP_200_OK)
async def health_check():
    """
    Health check endpoint
    """
    return HealthResponse(status="healthy", service="logging-pipeline")