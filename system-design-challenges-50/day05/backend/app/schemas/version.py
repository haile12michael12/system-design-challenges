"""Pydantic models for requirement versions"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class VersionBase(BaseModel):
    requirement_id: int
    version_number: int
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"
    status: Optional[str] = "draft"

class VersionCreate(VersionBase):
    pass

class VersionUpdate(VersionBase):
    pass

class VersionResponse(VersionBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True