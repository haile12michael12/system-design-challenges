from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from enum import Enum as PyEnum
from typing import Optional
import uuid

Base = declarative_base()


class RecommendationStatus(str, PyEnum):
    """Enumeration of recommendation statuses"""
    PENDING = "pending"
    APPLIED = "applied"
    ROLLED_BACK = "rolled_back"
    REJECTED = "rejected"


class Service(Base):
    """Model for storing service information"""
    __tablename__ = "services"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    owner = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __init__(self, name: str, owner: str, description: Optional[str] = None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.owner = owner
        self.description = description


class Recommendation(Base):
    """Model for storing cost optimization recommendations"""
    __tablename__ = "recommendations"
    
    id = Column(String, primary_key=True, index=True)
    service_id = Column(String, ForeignKey("services.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    estimated_savings = Column(Float, nullable=False)
    implementation_cost = Column(Float, nullable=False)
    priority = Column(Integer, nullable=False, default=1)  # 1-5 scale
    status = Column(Enum(RecommendationStatus), nullable=False, default=RecommendationStatus.PENDING)
    config_changes = Column(Text, nullable=True)  # JSON serialized config changes
    sla_impact = Column(Text, nullable=True)  # JSON serialized SLA impact analysis
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __init__(self, service_id: str, title: str, description: str, 
                 estimated_savings: float, implementation_cost: float,
                 priority: int = 1, config_changes: Optional[str] = None,
                 sla_impact: Optional[str] = None):
        self.id = str(uuid.uuid4())
        self.service_id = service_id
        self.title = title
        self.description = description
        self.estimated_savings = estimated_savings
        self.implementation_cost = implementation_cost
        self.priority = priority
        self.config_changes = config_changes
        self.sla_impact = sla_impact


class Simulation(Base):
    """Model for storing simulation results"""
    __tablename__ = "simulations"
    
    id = Column(String, primary_key=True, index=True)
    service_id = Column(String, ForeignKey("services.id"), nullable=False)
    scenario = Column(String, nullable=False)
    duration_hours = Column(Integer, nullable=False)
    cost_before = Column(Float, nullable=False)
    cost_after = Column(Float, nullable=False)
    performance_impact = Column(Float, nullable=False)  # Percentage change
    sla_compliance = Column(Boolean, nullable=False, default=True)
    results = Column(Text, nullable=True)  # JSON serialized detailed results
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __init__(self, service_id: str, scenario: str, duration_hours: int,
                 cost_before: float, cost_after: float, performance_impact: float,
                 sla_compliance: bool = True, results: Optional[str] = None):
        self.id = str(uuid.uuid4())
        self.service_id = service_id
        self.scenario = scenario
        self.duration_hours = duration_hours
        self.cost_before = cost_before
        self.cost_after = cost_after
        self.performance_impact = performance_impact
        self.sla_compliance = sla_compliance
        self.results = results


class ConfigChange(Base):
    """Model for storing configuration changes"""
    __tablename__ = "config_changes"
    
    id = Column(String, primary_key=True, index=True)
    service_id = Column(String, ForeignKey("services.id"), nullable=False)
    recommendation_id = Column(String, ForeignKey("recommendations.id"), nullable=True)
    change_type = Column(String, nullable=False)
    old_config = Column(Text, nullable=True)  # JSON serialized old config
    new_config = Column(Text, nullable=False)  # JSON serialized new config
    applied_by = Column(String, nullable=False)
    applied_at = Column(DateTime(timezone=True), server_default=func.now())
    rolled_back = Column(Boolean, nullable=False, default=False)
    rolled_back_at = Column(DateTime(timezone=True), nullable=True)
    
    def __init__(self, service_id: str, change_type: str, new_config: str,
                 applied_by: str, recommendation_id: Optional[str] = None,
                 old_config: Optional[str] = None):
        self.id = str(uuid.uuid4())
        self.service_id = service_id
        self.recommendation_id = recommendation_id
        self.change_type = change_type
        self.old_config = old_config
        self.new_config = new_config
        self.applied_by = applied_by