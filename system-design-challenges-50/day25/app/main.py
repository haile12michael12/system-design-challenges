from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Day 25 - Monitoring & Observability Suite")

class HealthResp(BaseModel):
    status: str = "ok"
    service: str = "day25"

@app.get("/health", response_model=HealthResp)
async def health():
    return HealthResp()

@app.get("/")
async def root():
    return {"message": "Welcome to Day 25 - Monitoring & Observability Suite"}

@app.get("/hello")
async def hello():
    return {"message": "Hello from day25"}
