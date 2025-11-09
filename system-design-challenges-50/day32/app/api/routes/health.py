from fastapi import APIRouter, status
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    service: str
    timestamp: Optional[datetime] = None
    
    class Config:
        orm_mode = True

@router.get("/", response_model=HealthResponse, status_code=status.HTTP_200_OK)
async def health_check():
    """
    Health check endpoint
    """
    return HealthResponse(
        status="healthy", 
        service="document-editor",
        timestamp=datetime.utcnow()
    )