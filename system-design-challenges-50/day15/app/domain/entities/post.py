from dataclasses import dataclass
from typing import Optional
from ..value_objects.post_id import PostId

@dataclass
class Post:
    id: PostId
    content: str
    author: str
    
    def __post_init__(self):
        if not self.content:
            raise ValueError("Content cannot be empty")
        if not self.author:
            raise ValueError("Author cannot be empty")