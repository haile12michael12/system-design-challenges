from fastapi import FastAPI
from app.routes import auth, feed, posts, health, admin

app = FastAPI(title="Feed Engine", version="0.1.0")

# Include routers
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(posts.router, prefix="/posts", tags=["posts"])
app.include_router(feed.router, prefix="/feed", tags=["feed"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])

@app.get("/")
async def root():
    return {"message": "Feed Engine API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)