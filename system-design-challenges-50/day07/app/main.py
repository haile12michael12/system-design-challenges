from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Day 7 - Stateful Multiplayer Game Lobby System")

class HealthResp(BaseModel):
    status: str = "ok"
    service: str = "day07"

@app.get("/health", response_model=HealthResp)
async def health():
    return HealthResp()

@app.get("/")
async def root():
    return {"message": "Welcome to Day 7 - Stateful Multiplayer Game Lobby System"}

@app.get("/hello")
async def hello():
    return {"message": "Hello from day07"}
