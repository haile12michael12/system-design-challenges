from fastapi import APIRouter, Depends
from app.schemas.common import SuccessResponse
from app.dependencies import get_redis

router = APIRouter()

@router.get("/", response_model=SuccessResponse)
async def health_check():
    return SuccessResponse(message="Feed Engine is running")

@router.get("/ready", response_model=SuccessResponse)
async def readiness_check(redis=Depends(get_redis)):
    # Check database and Redis connectivity
    try:
        redis.ping()
        # In a real implementation, we would also check database connectivity
        return SuccessResponse(message="Service is ready")
    except Exception:
        return SuccessResponse(success=False, message="Service not ready")