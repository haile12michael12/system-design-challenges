from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.api.health import router as health_router
from app.api.users import router as users_router
from app.api.posts import router as posts_router
from app.api.feed import router as feed_router
from app.api.media import router as media_router
from app.core.config import settings
from app.core.logging import logger
from app.db.session import init_db

# Create FastAPI app
app = FastAPI(
    title="Social Media API",
    description="A scalable social media platform API",
    version="1.0.0"
)

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
app.include_router(users_router, prefix="/api/v1/users", tags=["users"])
app.include_router(posts_router, prefix="/api/v1/posts", tags=["posts"])
app.include_router(feed_router, prefix="/api/v1/feed", tags=["feed"])
app.include_router(media_router, prefix="/api/v1/media", tags=["media"])

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    logger.info("Starting Social Media API...")
    
    # Initialize database
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
    
    logger.info("Social Media API started successfully")


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to the Social Media API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


# Health check endpoint
@app.get("/healthz")
async def healthz():
    """Kubernetes health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)