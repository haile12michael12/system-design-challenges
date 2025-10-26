from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Day 44 - Graph-DB Based Social Graph")

class HealthResp(BaseModel):
    status: str = "ok"
    service: str = "day44"

@app.get("/health", response_model=HealthResp)
async def health():
    return HealthResp()

@app.get("/")
async def root():
    return {"message": "Welcome to Day 44 - Graph-DB Based Social Graph"}

@app.get("/hello")
async def hello():
    return {"message": "Hello from day44"}
