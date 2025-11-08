from fastapi import FastAPI
from pydantic import BaseModel
from app.db.base import engine, Base
from app.db.models import User, Prompt, Submission, Grading

app = FastAPI(title="System Design Coach App")

# Create tables
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

class HealthResp(BaseModel):
    status: str = "ok"
    service: str = "system-design-coach"

@app.get("/health", response_model=HealthResp)
async def health():
    return HealthResp()

@app.get("/")
async def root():
    return {"message": "Welcome to System Design Coach App"}

@app.get("/hello")
async def hello():
    return {"message": "Hello from System Design Coach"}
