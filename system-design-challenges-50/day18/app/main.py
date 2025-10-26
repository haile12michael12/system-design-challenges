from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Day 18 - Latency-Aware News App")

class HealthResp(BaseModel):
    status: str = "ok"
    service: str = "day18"

@app.get("/health", response_model=HealthResp)
async def health():
    return HealthResp()

@app.get("/")
async def root():
    return {"message": "Welcome to Day 18 - Latency-Aware News App"}

@app.get("/hello")
async def hello():
    return {"message": "Hello from day18"}
