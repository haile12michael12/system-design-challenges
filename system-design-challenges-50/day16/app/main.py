from fastapi import FastAPI
from .routes import auth, health

app = FastAPI(title="Authentication Service")

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(health.router, prefix="/api/v1", tags=["health"])

@app.get("/")
async def root():
    return {"message": "Authentication Service"}
