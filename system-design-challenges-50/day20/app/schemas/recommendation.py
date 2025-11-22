from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class RecommendationStatus(str, Enum):
    """Recommendation status enumeration"""
    PENDING = "pending"
    APPLIED = "applied"
    ROLLED_BACK = "rolled_back"
    REJECTED = "rejected"


class Recommendation(BaseModel):
    """Schema for cost optimization recommendation"""
    id: str
    service_id: str
    title: str
    description: str
    estimated_savings: float
    implementation_cost: float
    priority: int = 1  # 1-5 scale
    status: RecommendationStatus = RecommendationStatus.PENDING
    config_changes: Optional[str] = None  # JSON serialized config changes
    sla_impact: Optional[str] = None  # JSON serialized SLA impact analysis
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class RecommendationRequest(BaseModel):
    """Schema for recommendation request"""
    service_id: str
    budget_constraints: Optional[Dict[str, Any]] = None
    priority_filter: Optional[int] = None  # Only recommendations with priority >= this value


class RecommendationResponse(BaseModel):
    """Schema for recommendation response"""
    recommendations: List[Recommendation]
    generated_at: Optional[datetime] = None


class RecommendationApplyRequest(BaseModel):
    """Schema for applying a recommendation"""
    service_id: str
    recommendation_id: str
    parameters: Optional[Dict[str, Any]] = None


class SimulationScenario(BaseModel):
    """Schema for simulation scenario"""
    name: str
    description: Optional[str] = None
    changes: Dict[str, Any]  # Resource changes to simulate


class SimulationRequest(BaseModel):
    """Schema for simulation request"""
    service_id: str
    scenarios: List[SimulationScenario]
    duration_hours: int = 24


class SimulationResult(BaseModel):
    """Schema for simulation result"""
    scenario: str
    description: Optional[str] = None
    changes: Dict[str, Any]
    cost_before: float
    cost_after: float
    estimated_savings: float
    performance_impact: float  # Percentage change
    sla_compliance: bool
    duration_hours: int
    executed_at: Optional[datetime] = None


class SimulationResponse(BaseModel):
    """Schema for simulation response"""
    service_id: str
    scenarios: List[SimulationResult]
    generated_at: Optional[datetime] = None