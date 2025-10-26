from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Day 46 - Time-Series Metrics Store")

class HealthResp(BaseModel):
    status: str = "ok"
    service: str = "day46"

@app.get("/health", response_model=HealthResp)
async def health():
    return HealthResp()

@app.get("/")
async def root():
    return {"message": "Welcome to Day 46 - Time-Series Metrics Store"}

@app.get("/hello")
async def hello():
    return {"message": "Hello from day46"}
