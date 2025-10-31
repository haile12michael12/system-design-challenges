from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Question(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Feedback(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    question_id: int
    rating: int  # 1-5 scale
    comment: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Analytics(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    question_id: int
    views: int = 0
    avg_rating: float = 0.0
    total_feedback: int = 0
    last_updated: datetime = Field(default_factory=datetime.utcnow)