from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class HealthResponse(BaseModel):
    status: str
    service: str
    timestamp: Optional[datetime] = None
    
    class Config:
        orm_mode = True