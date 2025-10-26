from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Day 21 - Design Instagram Simulator")

class HealthResp(BaseModel):
    status: str = "ok"
    service: str = "day21"

@app.get("/health", response_model=HealthResp)
async def health():
    return HealthResp()

@app.get("/")
async def root():
    return {"message": "Welcome to Day 21 - Design Instagram Simulator"}

@app.get("/hello")
async def hello():
    return {"message": "Hello from day21"}
