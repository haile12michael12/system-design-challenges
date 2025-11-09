from fastapi import FastAPI
from app.core.config import settings
from app.core.logger import setup_logging
from app.db.session import engine, Base

# Setup logging
setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="Real-Time Collaborative Document Editor"
)

# Import routers
from app.api.routes import health, documents
from app.api.ws import editor_ws

# Include routers
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(documents.router, prefix="/api", tags=["documents"])
app.include_router(editor_ws.router)

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}

@app.on_event("startup")
async def startup_event():
    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print(f"{settings.PROJECT_NAME} started successfully")
