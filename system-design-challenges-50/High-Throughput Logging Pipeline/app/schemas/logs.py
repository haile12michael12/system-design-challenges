from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List, Union
from datetime import datetime
from enum import Enum

class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class LogIn(BaseModel):
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)
    level: LogLevel = LogLevel.INFO
    message: str
    service: str
    tenant_id: Optional[str] = None
    trace_id: Optional[str] = None
    span_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class LogOut(LogIn):
    id: str
    created_at: datetime
    
    class Config:
        orm_mode = True

class LogBatchIn(BaseModel):
    logs: List[LogIn]
    
class LogQuery(BaseModel):
    service: Optional[str] = None
    tenant_id: Optional[str] = None
    level: Optional[LogLevel] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    limit: Optional[int] = 100
    offset: Optional[int] = 0