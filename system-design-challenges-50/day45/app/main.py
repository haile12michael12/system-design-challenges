from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Day 45 - Massively Concurrent Websocket Hub")

class HealthResp(BaseModel):
    status: str = "ok"
    service: str = "day45"

@app.get("/health", response_model=HealthResp)
async def health():
    return HealthResp()

@app.get("/")
async def root():
    return {"message": "Welcome to Day 45 - Massively Concurrent Websocket Hub"}

@app.get("/hello")
async def hello():
    return {"message": "Hello from day45"}
