from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Day 26 - Hybrid Strong + Eventual Consistency Platform")

class HealthResp(BaseModel):
    status: str = "ok"
    service: str = "day26"

@app.get("/health", response_model=HealthResp)
async def health():
    return HealthResp()

@app.get("/")
async def root():
    return {"message": "Welcome to Day 26 - Hybrid Strong + Eventual Consistency Platform"}

@app.get("/hello")
async def hello():
    return {"message": "Hello from day26"}
