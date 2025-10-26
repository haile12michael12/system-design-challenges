from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Day 39 - Privacy-Preserving Analytics")

class HealthResp(BaseModel):
    status: str = "ok"
    service: str = "day39"

@app.get("/health", response_model=HealthResp)
async def health():
    return HealthResp()

@app.get("/")
async def root():
    return {"message": "Welcome to Day 39 - Privacy-Preserving Analytics"}

@app.get("/hello")
async def hello():
    return {"message": "Hello from day39"}
