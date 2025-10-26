from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Day 8 - Database Migration Simulator")

class HealthResp(BaseModel):
    status: str = "ok"
    service: str = "day08"

@app.get("/health", response_model=HealthResp)
async def health():
    return HealthResp()

@app.get("/")
async def root():
    return {"message": "Welcome to Day 8 - Database Migration Simulator"}

@app.get("/hello")
async def hello():
    return {"message": "Hello from day08"}
