from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Day 48 - Data Lake Ingestion Framework")

class HealthResp(BaseModel):
    status: str = "ok"
    service: str = "day48"

@app.get("/health", response_model=HealthResp)
async def health():
    return HealthResp()

@app.get("/")
async def root():
    return {"message": "Welcome to Day 48 - Data Lake Ingestion Framework"}

@app.get("/hello")
async def hello():
    return {"message": "Hello from day48"}
