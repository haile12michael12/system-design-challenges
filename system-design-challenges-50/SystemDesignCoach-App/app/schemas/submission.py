from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SubmissionBase(BaseModel):
    prompt_id: int
    user_id: int
    diagram_data: str
    explanation: str

class SubmissionCreate(SubmissionBase):
    pass

class SubmissionUpdate(BaseModel):
    diagram_data: Optional[str] = None
    explanation: Optional[str] = None

class SubmissionInDB(SubmissionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Submission(SubmissionInDB):
    pass