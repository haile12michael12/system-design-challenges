from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Day 11 - Auto-Scaler Visualizer")

class HealthResp(BaseModel):
    status: str = "ok"
    service: str = "day11"

@app.get("/health", response_model=HealthResp)
async def health():
    return HealthResp()

@app.get("/")
async def root():
    return {"message": "Welcome to Day 11 - Auto-Scaler Visualizer"}

@app.get("/hello")
async def hello():
    return {"message": "Hello from day11"}
