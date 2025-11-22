from typing import Optional
from pydantic import BaseModel


class Pagination(BaseModel):
    page: int = 1
    size: int = 20
    offset: Optional[int] = None
    
    def __init__(self, **data):
        super().__init__(**data)
        self.offset = (self.page - 1) * self.size
    
    def limit(self) -> int:
        return self.size
    
    def offset_value(self) -> int:
        return self.offset
    
    def has_next_page(self, total_count: int) -> bool:
        return self.offset + self.size < total_count
    
    def has_previous_page(self) -> bool:
        return self.page > 1
    
    def total_pages(self, total_count: int) -> int:
        return (total_count + self.size - 1) // self.size