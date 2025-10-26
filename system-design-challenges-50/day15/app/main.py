from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Day 15 - Read vs Write Optimized Social App")

class HealthResp(BaseModel):
    status: str = "ok"
    service: str = "day15"

@app.get("/health", response_model=HealthResp)
async def health():
    return HealthResp()

@app.get("/")
async def root():
    return {"message": "Welcome to Day 15 - Read vs Write Optimized Social App"}

@app.get("/hello")
async def hello():
    return {"message": "Hello from day15"}
