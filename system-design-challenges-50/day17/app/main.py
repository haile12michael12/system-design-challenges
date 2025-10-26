from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Day 17 - Eventually Consistent Social Feed")

class HealthResp(BaseModel):
    status: str = "ok"
    service: str = "day17"

@app.get("/health", response_model=HealthResp)
async def health():
    return HealthResp()

@app.get("/")
async def root():
    return {"message": "Welcome to Day 17 - Eventually Consistent Social Feed"}

@app.get("/hello")
async def hello():
    return {"message": "Hello from day17"}
