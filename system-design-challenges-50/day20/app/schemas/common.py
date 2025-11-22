from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class HealthCheck(BaseModel):
    """Schema for health check response"""
    status: str
    timestamp: str
    service: str


class ErrorResponse(BaseModel):
    """Schema for error response"""
    detail: str
    status_code: int
    timestamp: str


class SuccessResponse(BaseModel):
    """Schema for success response"""
    status: str
    message: str
    data: Optional[Dict[str, Any]] = None
    timestamp: str


class Pagination(BaseModel):
    """Schema for pagination"""
    page: int
    size: int
    total: int
    has_next: bool
    has_prev: bool


class PaginatedResponse(BaseModel):
    """Schema for paginated response"""
    data: list
    pagination: Pagination
    timestamp: str


class ConfigChange(BaseModel):
    """Schema for configuration change"""
    id: str
    service_id: str
    change_type: str
    old_config: Optional[str] = None
    new_config: str
    applied_by: str
    applied_at: datetime
    rolled_back: bool = False
    rolled_back_at: Optional[datetime] = None


class BudgetStatus(BaseModel):
    """Schema for budget status"""
    service_id: str
    budget_id: str
    budget_amount: float
    spent_amount: float
    remaining_amount: float
    percentage_used: float
    status: str
    forecast_overspend: bool
    forecast_overspend_amount: float


class CostAnomaly(BaseModel):
    """Schema for cost anomaly"""
    anomaly_id: str
    timestamp: str
    resource_id: str
    expected_cost: float
    actual_cost: float
    variance: float
    variance_percentage: float