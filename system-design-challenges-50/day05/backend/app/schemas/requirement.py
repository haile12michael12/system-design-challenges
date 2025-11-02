"""Pydantic models for requirements"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RequirementBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"
    status: Optional[str] = "draft"
    project_id: Optional[int] = None

class RequirementCreate(RequirementBase):
    pass

class RequirementUpdate(RequirementBase):
    title: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None

class RequirementResponse(RequirementBase):
    id: int
    version: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True