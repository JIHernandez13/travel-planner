import sys
from pathlib import Path

# Add parent directory to path to import config, database, etc.
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from app.api import auth, trips, activities

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Travel Planner API - Plan and organize your trips"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "Welcome to Travel Planner API",
        "version": settings.VERSION,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# Include API routers
app.include_router(auth.router, prefix=f"{settings.API_V1_PREFIX}/auth",
                   tags=["authentication"])
app.include_router(trips.router, prefix=f"{settings.API_V1_PREFIX}/trips",
                   tags=["trips"])
app.include_router(activities.router, prefix=f"{settings.API_V1_PREFIX}/activities",
                   tags=["activities"])
