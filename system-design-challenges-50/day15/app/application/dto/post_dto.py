from dataclasses import dataclass
from typing import Optional

@dataclass
class PostDTO:
    id: str
    content: str
    author: str
    created_at: Optional[str] = None