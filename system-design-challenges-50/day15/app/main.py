from fastapi import FastAPI
from .config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG
)


@app.get("/")
async def root():
    return {"message": "Post Service API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

