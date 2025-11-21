from pydantic import BaseModel
from typing import Optional

class PostResponse(BaseModel):
    id: str
    content: str
    author: str