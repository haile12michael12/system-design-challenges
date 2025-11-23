from pydantic import BaseModel
from typing import Optional, Any, Dict

class SuccessResponse(BaseModel):
    success: bool = True
    message: str = ""
    data: Optional[Any] = None

class ErrorResponse(BaseModel):
    success: bool = False
    error: str = ""
    details: Optional[Dict[str, Any]] = None

class PaginationMeta(BaseModel):
    page: int
    per_page: int
    total: int
    has_next: bool
    has_prev: bool