import json
from typing import Dict, Any
from ...db.models import PostModel

class PostCacheSerializerV1:
    @staticmethod
    def serialize(post: PostModel) -> str:
        data = {
            "id": post.id,
            "content": post.content,
            "author": post.author,
            "created_at": post.created_at.isoformat() if post.created_at else None
        }
        return json.dumps(data)
    
    @staticmethod
    def deserialize(data: str) -> Dict[str, Any]:
        return json.loads(data)