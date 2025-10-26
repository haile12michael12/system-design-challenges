from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Day 4 - Requirements Analyzer CLI")

class HealthResp(BaseModel):
    status: str = "ok"
    service: str = "day04"

@app.get("/health", response_model=HealthResp)
async def health():
    return HealthResp()

@app.get("/")
async def root():
    return {"message": "Welcome to Day 4 - Requirements Analyzer CLI"}

@app.get("/hello")
async def hello():
    return {"message": "Hello from day04"}
