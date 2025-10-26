from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Day 23 - Event-Driven Order Processing System")

class HealthResp(BaseModel):
    status: str = "ok"
    service: str = "day23"

@app.get("/health", response_model=HealthResp)
async def health():
    return HealthResp()

@app.get("/")
async def root():
    return {"message": "Welcome to Day 23 - Event-Driven Order Processing System"}

@app.get("/hello")
async def hello():
    return {"message": "Hello from day23"}
