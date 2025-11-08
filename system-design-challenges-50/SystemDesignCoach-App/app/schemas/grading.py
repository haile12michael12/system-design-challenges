from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class GradingBase(BaseModel):
    submission_id: int
    score: float
    feedback: str

class GradingCreate(GradingBase):
    pass

class GradingUpdate(BaseModel):
    score: Optional[float] = None
    feedback: Optional[str] = None

class GradingInDB(GradingBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Grading(GradingInDB):
    pass