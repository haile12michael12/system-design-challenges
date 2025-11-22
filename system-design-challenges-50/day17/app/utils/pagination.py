from typing import Optional
from pydantic import BaseModel, Field, validator


class PaginationParams(BaseModel):
    """Pagination parameters."""
    page: int = Field(1, ge=1, description="Page number (starting from 1)")
    size: int = Field(10, ge=1, le=100, description="Page size (max 100)")
    
    @validator('size')
    def validate_size(cls, v):
        """Validate page size."""
        if v > 100:
            raise ValueError('Page size cannot exceed 100')
        return v
    
    @validator('page')
    def validate_page(cls, v):
        """Validate page number."""
        if v < 1:
            raise ValueError('Page number must be at least 1')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "page": 1,
                "size": 10
            }
        }


class PaginatedResponse(BaseModel):
    """Base class for paginated responses."""
    page: int = Field(..., ge=1, description="Current page number")
    size: int = Field(..., ge=1, le=100, description="Page size")
    total: int = Field(..., ge=0, description="Total number of items")
    pages: int = Field(..., ge=0, description="Total number of pages")
    
    @validator('size')
    def validate_size(cls, v):
        """Validate page size."""
        if v > 100:
            raise ValueError('Page size cannot exceed 100')
        return v
    
    @validator('page')
    def validate_page(cls, v):
        """Validate page number."""
        if v < 1:
            raise ValueError('Page number must be at least 1')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "page": 1,
                "size": 10,
                "total": 100,
                "pages": 10
            }
        }