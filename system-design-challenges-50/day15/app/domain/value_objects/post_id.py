from dataclasses import dataclass
import uuid

@dataclass(frozen=True)
class PostId:
    value: str
    
    def __post_init__(self):
        if not self.value:
            raise ValueError("Post ID cannot be empty")
    
    @classmethod
    def new(cls) -> 'PostId':
        return cls(str(uuid.uuid4()))