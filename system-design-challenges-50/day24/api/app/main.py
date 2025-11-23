from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.health import router as health_router
from app.api.simulate import router as simulate_router
from app.websocket.regions import router as websocket_router

app = FastAPI(title="Failover Dashboard API", version="0.1.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router, prefix="/health", tags=["health"])
app.include_router(simulate_router, prefix="/simulate", tags=["simulate"])
app.include_router(websocket_router, prefix="/ws", tags=["websocket"])

@app.get("/")
async def root():
    return {"message": "Failover Dashboard API"}