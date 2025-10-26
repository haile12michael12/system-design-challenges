from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Day 13 - High-Durability Payment Gateway")

class HealthResp(BaseModel):
    status: str = "ok"
    service: str = "day13"

@app.get("/health", response_model=HealthResp)
async def health():
    return HealthResp()

@app.get("/")
async def root():
    return {"message": "Welcome to Day 13 - High-Durability Payment Gateway"}

@app.get("/hello")
async def hello():
    return {"message": "Hello from day13"}
