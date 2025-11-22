from typing import Optional
from pydantic import BaseModel, Field


class SuccessResponse(BaseModel):
    """Schema for generic success response."""
    success: bool = Field(True, description="Operation success status")
    message: str = Field(..., description="Success message")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "Operation completed successfully"
            }
        }


class ErrorResponse(BaseModel):
    """Schema for generic error response."""
    success: bool = Field(False, description="Operation success status")
    error: str = Field(..., description="Error message")
    details: Optional[dict] = Field(None, description="Additional error details")
    
    class Config:
        schema_extra = {
            "example": {
                "success": False,
                "error": "An error occurred",
                "details": {
                    "code": "ERROR_CODE",
                    "description": "Detailed error description"
                }
            }
        }


class HealthResponse(BaseModel):
    """Schema for health check response."""
    status: str = Field(..., description="Service status")
    service: str = Field(..., description="Service name")
    version: Optional[str] = Field(None, description="Service version")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "service": "feed-service",
                "version": "1.0.0"
            }
        }


class Token(BaseModel):
    """Schema for JWT token."""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field("bearer", description="Token type")
    
    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }


class TokenData(BaseModel):
    """Schema for token data."""
    user_id: Optional[str] = Field(None, description="User ID")
    username: Optional[str] = Field(None, description="Username")