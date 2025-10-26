from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Day 27 - Dynamic Cache Invalidation AI Agent")

class HealthResp(BaseModel):
    status: str = "ok"
    service: str = "day27"

@app.get("/health", response_model=HealthResp)
async def health():
    return HealthResp()

@app.get("/")
async def root():
    return {"message": "Welcome to Day 27 - Dynamic Cache Invalidation AI Agent"}

@app.get("/hello")
async def hello():
    return {"message": "Hello from day27"}
