from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Day 24 - Multi-Region Failover Simulation")

class HealthResp(BaseModel):
    status: str = "ok"
    service: str = "day24"

@app.get("/health", response_model=HealthResp)
async def health():
    return HealthResp()

@app.get("/")
async def root():
    return {"message": "Welcome to Day 24 - Multi-Region Failover Simulation"}

@app.get("/hello")
async def hello():
    return {"message": "Hello from day24"}
