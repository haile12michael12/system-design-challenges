from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Day 32 - Real-Time Collaboration Editor")

class HealthResp(BaseModel):
    status: str = "ok"
    service: str = "day32"

@app.get("/health", response_model=HealthResp)
async def health():
    return HealthResp()

@app.get("/")
async def root():
    return {"message": "Welcome to Day 32 - Real-Time Collaboration Editor"}

@app.get("/hello")
async def hello():
    return {"message": "Hello from day32"}
