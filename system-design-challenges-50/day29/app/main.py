from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Day 29 - Resilient Multi-Service Deployment Simulator")

class HealthResp(BaseModel):
    status: str = "ok"
    service: str = "day29"

@app.get("/health", response_model=HealthResp)
async def health():
    return HealthResp()

@app.get("/")
async def root():
    return {"message": "Welcome to Day 29 - Resilient Multi-Service Deployment Simulator"}

@app.get("/hello")
async def hello():
    return {"message": "Hello from day29"}
