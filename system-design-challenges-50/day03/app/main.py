from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import asyncio

# Import routers
from app.analytics import router as analytics_router

app = FastAPI(title="Day 3 - Feedback-Driven System Design Portal")

# Include routers
app.include_router(analytics_router)

# Models
class HealthResp(BaseModel):
    status: str = "ok"
    service: str = "day03"

class QuestionBase(BaseModel):
    title: str
    content: str

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: int
    created_at: datetime
    updated_at: datetime

class FeedbackBase(BaseModel):
    question_id: int
    rating: int  # 1-5 scale
    comment: Optional[str] = None

class FeedbackCreate(FeedbackBase):
    pass

class Feedback(FeedbackBase):
    id: int
    created_at: datetime

# In-memory storage (in production, this would be in a database)
questions_db: dict[int, Question] = {}
feedback_db: dict[int, list[Feedback]] = {}
next_question_id = 1
next_feedback_id = 1

@app.get("/health", response_model=HealthResp)
async def health():
    return HealthResp()

@app.get("/")
async def root():
    return {"message": "Welcome to Day 3 - Feedback-Driven System Design Portal"}

@app.get("/hello")
async def hello():
    return {"message": "Hello from day03"}

# Question endpoints
@app.post("/questions/", response_model=Question)
async def create_question(question: QuestionCreate):
    global next_question_id
    new_question = Question(
        id=next_question_id,
        title=question.title,
        content=question.content,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    questions_db[next_question_id] = new_question
    next_question_id += 1
    return new_question

@app.get("/questions/", response_model=List[Question])
async def get_questions():
    return list(questions_db.values())

@app.get("/questions/{question_id}", response_model=Question)
async def get_question(question_id: int):
    if question_id not in questions_db:
        raise HTTPException(status_code=404, detail="Question not found")
    return questions_db[question_id]

# Feedback endpoints
@app.post("/feedback/", response_model=dict)
async def submit_feedback(feedback: FeedbackCreate):
    global next_feedback_id
    if feedback.question_id not in questions_db:
        raise HTTPException(status_code=404, detail="Question not found")
    
    new_feedback = Feedback(
        id=next_feedback_id,
        question_id=feedback.question_id,
        rating=feedback.rating,
        comment=feedback.comment,
        created_at=datetime.utcnow()
    )
    
    if feedback.question_id not in feedback_db:
        feedback_db[feedback.question_id] = []
    feedback_db[feedback.question_id].append(new_feedback)
    next_feedback_id += 1
    
    return {"message": "Feedback submitted successfully"}

@app.get("/feedback/{question_id}", response_model=List[Feedback])
async def get_feedback(question_id: int):
    if question_id not in feedback_db:
        return []
    return feedback_db[question_id]