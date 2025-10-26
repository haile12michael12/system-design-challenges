from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Day 22 - Real-Time Analytics Pipeline")

class HealthResp(BaseModel):
    status: str = "ok"
    service: str = "day22"

@app.get("/health", response_model=HealthResp)
async def health():
    return HealthResp()

@app.get("/")
async def root():
    return {"message": "Welcome to Day 22 - Real-Time Analytics Pipeline"}

@app.get("/hello")
async def hello():
    return {"message": "Hello from day22"}
