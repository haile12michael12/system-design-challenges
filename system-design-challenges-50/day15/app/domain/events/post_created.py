from dataclasses import dataclass
from datetime import datetime
from ..value_objects.post_id import PostId

@dataclass
class PostCreated:
    post_id: PostId
    content: str
    author: str
    created_at: datetime
    
    def __post_init__(self):
        if not self.content:
            raise ValueError("Content cannot be empty")
        if not self.author:
            raise ValueError("Author cannot be empty")