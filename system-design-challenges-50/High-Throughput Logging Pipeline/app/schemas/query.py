from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.schemas.logs import LogLevel

class LogQueryParams(BaseModel):
    service: Optional[str] = None
    tenant_id: Optional[str] = None
    level: Optional[LogLevel] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    limit: Optional[int] = 100
    offset: Optional[int] = 0

class LogSearchResult(BaseModel):
    id: str
    timestamp: datetime
    level: LogLevel
    message: str
    service: str
    tenant_id: Optional[str] = None
    trace_id: Optional[str] = None
    span_id: Optional[str] = None

class LogQueryResponse(BaseModel):
    results: List[LogSearchResult]
    total: int
    limit: int
    offset: int