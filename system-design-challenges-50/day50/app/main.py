from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Day 50 - Immutable Infrastructure Deployer")

class HealthResp(BaseModel):
    status: str = "ok"
    service: str = "day50"

@app.get("/health", response_model=HealthResp)
async def health():
    return HealthResp()

@app.get("/")
async def root():
    return {"message": "Welcome to Day 50 - Immutable Infrastructure Deployer"}

@app.get("/hello")
async def hello():
    return {"message": "Hello from day50"}
