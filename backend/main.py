from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from database import Base, engine
from router_auth import router as auth_router

# Create database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=(
        "Travel Planner API - Plan and organize your trips"
    ),
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=[
        "GET", "POST", "PUT", "DELETE", "OPTIONS",
    ],
    allow_headers=["Content-Type", "Authorization"],
)

# Include auth router
app.include_router(
    auth_router,
    prefix="/api/v1/auth",
    tags=["authentication"],
)


@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "Welcome to Travel Planner API",
        "version": settings.VERSION,
        "status": "running",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# TODO: Import and include routers for trips and activities
# app.include_router(trips.router, prefix="/api/v1/trips",
#                    tags=["trips"])
# app.include_router(activities.router,
#                    prefix="/api/v1/activities",
#                    tags=["activities"])
