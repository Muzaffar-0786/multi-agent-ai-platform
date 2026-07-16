from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import create_tables

from routes import router

from config import settings



# ==========================================================
# Application Lifespan
# ==========================================================

@asynccontextmanager
async def lifespan(
    app: FastAPI,
):
    """
    Application startup and shutdown events.
    """

    # Startup
    create_tables()

    yield

    # Shutdown
    pass



# ==========================================================
# FastAPI Application
# ==========================================================

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)



# ==========================================================
# Routes
# ==========================================================

app.include_router(
    router
)



# ==========================================================
# Root Endpoint
# ==========================================================

@app.get("/")
def root():

    return {
        "message": "Multi-Agent AI Platform is running.",
        "version": settings.APP_VERSION,
    }



# ==========================================================
# Server Check
# ==========================================================

@app.get("/status")
def status_check():

    return {
        "app": settings.APP_NAME,
        "status": "healthy",
    }
