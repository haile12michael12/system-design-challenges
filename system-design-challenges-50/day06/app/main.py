from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Day 6 - Client-Server Chat Application")

class HealthResp(BaseModel):
    status: str = "ok"
    service: str = "day06"

@app.get("/health", response_model=HealthResp)
async def health():
    return HealthResp()

@app.get("/")
async def root():
    return {"message": "Welcome to Day 6 - Client-Server Chat Application"}

@app.get("/hello")
async def hello():
    return {"message": "Hello from day06"}
