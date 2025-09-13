"""
222.place Matchmaking Platform API
Main application entry point
"""

import os
import sys
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import structlog
import uvicorn
from prometheus_client import make_asgi_app

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.settings import settings
from config.database import init_db
from routes import auth, onboarding, matching, events, social, health
from utils.logging import setup_logging

# Setup structured logging
setup_logging()
logger = structlog.get_logger()

# Create FastAPI application
app = FastAPI(
    title="222.place Matchmaking API",
    description="A privacy-first matchmaking platform API",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)

# Trusted hosts middleware for security
if settings.TRUSTED_HOSTS:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.TRUSTED_HOSTS
    )

# Include routers
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(onboarding.router, prefix="/onboarding", tags=["onboarding"])
app.include_router(matching.router, prefix="/matches", tags=["matching"])
app.include_router(events.router, prefix="/events", tags=["events"])
app.include_router(social.router, prefix="/social", tags=["social"])

# Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    logger.info("Starting 222.place Matchmaking API", version="1.0.0")
    
    # Initialize database
    await init_db()
    logger.info("Database initialized")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    logger.info("Shutting down 222.place Matchmaking API")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors."""
    logger.error(
        "Unhandled exception",
        path=request.url.path,
        method=request.method,
        exception=str(exc),
        exc_info=True
    )
    
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error_id": "INTERNAL_ERROR"
        }
    )

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "222.place Matchmaking API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs" if settings.DEBUG else "disabled"
    }

if __name__ == "__main__":
    # Run the application
    uvicorn.run(
        "app:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
        workers=1 if settings.DEBUG else settings.API_WORKERS
    )