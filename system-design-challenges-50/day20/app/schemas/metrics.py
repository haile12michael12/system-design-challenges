from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime


class MetricsRequest(BaseModel):
    """Schema for metrics request"""
    service_id: str
    metric_names: List[str]
    start_time: str
    end_time: str
    aggregation: str = "avg"


class MetricValue(BaseModel):
    """Schema for individual metric value"""
    timestamp: str
    value: float


class MetricData(BaseModel):
    """Schema for metric data"""
    values: List[MetricValue]
    aggregation: str
    unit: str


class MetricsResponse(BaseModel):
    """Schema for metrics response"""
    service_id: str
    metrics: Dict[str, MetricData]
    query_time: str


class ServiceHealth(BaseModel):
    """Schema for service health"""
    service_id: str
    status: str
    timestamp: str


class PerformanceMetrics(BaseModel):
    """Schema for performance metrics"""
    service_id: str
    time_range: str
    metrics: Dict[str, Any]
    timestamp: str


class ResourceUtilization(BaseModel):
    """Schema for resource utilization"""
    service_id: str
    resources: Dict[str, Any]
    timestamp: str


class Alert(BaseModel):
    """Schema for alert"""
    alert_id: str
    name: str
    severity: str
    status: str
    triggered_at: str
    description: str