from dataclasses import dataclass
from ...domain.value_objects.post_id import PostId

@dataclass
class CreatePostCommand:
    content: str
    author: str