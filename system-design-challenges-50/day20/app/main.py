from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Day 20 - Cost-Performance Optimizer")

class HealthResp(BaseModel):
    status: str = "ok"
    service: str = "day20"

@app.get("/health", response_model=HealthResp)
async def health():
    return HealthResp()

@app.get("/")
async def root():
    return {"message": "Welcome to Day 20 - Cost-Performance Optimizer"}

@app.get("/hello")
async def hello():
    return {"message": "Hello from day20"}
