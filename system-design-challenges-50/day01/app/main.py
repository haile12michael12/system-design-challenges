from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="Instagram Feed Service"
)

# Import routers
from app.api import routes_health, routes_feed, routes_users

# Include routers
app.include_router(routes_health.router, prefix="/health", tags=["health"])
app.include_router(routes_feed.router, prefix="/feed", tags=["feed"])
app.include_router(routes_users.router, prefix="/users", tags=["users"])

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}

@app.on_event("startup")
async def startup_event():
    print(f"{settings.PROJECT_NAME} started successfully")
