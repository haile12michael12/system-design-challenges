from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Day 41 - Edge-Cached CDN Prototype")

class HealthResp(BaseModel):
    status: str = "ok"
    service: str = "day41"

@app.get("/health", response_model=HealthResp)
async def health():
    return HealthResp()

@app.get("/")
async def root():
    return {"message": "Welcome to Day 41 - Edge-Cached CDN Prototype"}

@app.get("/hello")
async def hello():
    return {"message": "Hello from day41"}
