from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Day 49 - Cost-Aware Autoscaler")

class HealthResp(BaseModel):
    status: str = "ok"
    service: str = "day49"

@app.get("/health", response_model=HealthResp)
async def health():
    return HealthResp()

@app.get("/")
async def root():
    return {"message": "Welcome to Day 49 - Cost-Aware Autoscaler"}

@app.get("/hello")
async def hello():
    return {"message": "Hello from day49"}
