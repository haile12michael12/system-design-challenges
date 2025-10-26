from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Day 9 - Multi-Level Cache System")

class HealthResp(BaseModel):
    status: str = "ok"
    service: str = "day09"

@app.get("/health", response_model=HealthResp)
async def health():
    return HealthResp()

@app.get("/")
async def root():
    return {"message": "Welcome to Day 9 - Multi-Level Cache System"}

@app.get("/hello")
async def hello():
    return {"message": "Hello from day09"}
