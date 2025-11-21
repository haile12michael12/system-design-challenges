from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Token(BaseModel):
    id: int
    user_id: int
    token: str
    token_type: str
    is_revoked: bool = False
    expires_at: datetime
    created_at: datetime

    class Config:
        orm_mode = True