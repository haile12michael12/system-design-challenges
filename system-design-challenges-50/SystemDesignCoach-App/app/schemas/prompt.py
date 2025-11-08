from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PromptBase(BaseModel):
    title: str
    description: str
    difficulty: str

class PromptCreate(PromptBase):
    pass

class PromptUpdate(PromptBase):
    pass

class PromptInDB(PromptBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Prompt(PromptInDB):
    pass