from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Day 3 - Feedback-Driven System Design Portal")

class HealthResp(BaseModel):
    status: str = "ok"
    service: str = "day03"

@app.get("/health", response_model=HealthResp)
async def health():
    return HealthResp()

@app.get("/")
async def root():
    return {"message": "Welcome to Day 3 - Feedback-Driven System Design Portal"}

@app.get("/hello")
async def hello():
    return {"message": "Hello from day03"}
