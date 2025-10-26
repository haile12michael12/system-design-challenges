from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Day 37 - Search-as-a-Service Prototype")

class HealthResp(BaseModel):
    status: str = "ok"
    service: str = "day37"

@app.get("/health", response_model=HealthResp)
async def health():
    return HealthResp()

@app.get("/")
async def root():
    return {"message": "Welcome to Day 37 - Search-as-a-Service Prototype"}

@app.get("/hello")
async def hello():
    return {"message": "Hello from day37"}
