from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Day 36 - Feature Flagging Service")

class HealthResp(BaseModel):
    status: str = "ok"
    service: str = "day36"

@app.get("/health", response_model=HealthResp)
async def health():
    return HealthResp()

@app.get("/")
async def root():
    return {"message": "Welcome to Day 36 - Feature Flagging Service"}

@app.get("/hello")
async def hello():
    return {"message": "Hello from day36"}
