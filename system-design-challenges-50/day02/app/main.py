from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Day 2 - Weather Dashboard (Non-Functional Requirements Focus)")

class HealthResp(BaseModel):
    status: str = "ok"
    service: str = "day02"

@app.get("/health", response_model=HealthResp)
async def health():
    return HealthResp()

@app.get("/")
async def root():
    return {"message": "Welcome to Day 2 - Weather Dashboard (Non-Functional Requirements Focus)"}

@app.get("/hello")
async def hello():
    return {"message": "Hello from day02"}
