from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Day 5 - Scalable Requirements Tracker")

class HealthResp(BaseModel):
    status: str = "ok"
    service: str = "day05"

@app.get("/health", response_model=HealthResp)
async def health():
    return HealthResp()

@app.get("/")
async def root():
    return {"message": "Welcome to Day 5 - Scalable Requirements Tracker"}

@app.get("/hello")
async def hello():
    return {"message": "Hello from day05"}
