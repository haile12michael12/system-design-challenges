from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Day 12 - CAP Trade-Off Explorer")

class HealthResp(BaseModel):
    status: str = "ok"
    service: str = "day12"

@app.get("/health", response_model=HealthResp)
async def health():
    return HealthResp()

@app.get("/")
async def root():
    return {"message": "Welcome to Day 12 - CAP Trade-Off Explorer"}

@app.get("/hello")
async def hello():
    return {"message": "Hello from day12"}
