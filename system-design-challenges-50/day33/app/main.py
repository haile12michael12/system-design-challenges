from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Day 33 - Geo-Distributed Key-Value Store")

class HealthResp(BaseModel):
    status: str = "ok"
    service: str = "day33"

@app.get("/health", response_model=HealthResp)
async def health():
    return HealthResp()

@app.get("/")
async def root():
    return {"message": "Welcome to Day 33 - Geo-Distributed Key-Value Store"}

@app.get("/hello")
async def hello():
    return {"message": "Hello from day33"}
