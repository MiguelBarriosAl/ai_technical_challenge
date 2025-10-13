"""
Travel Assistant API - Main Application
FastAPI application with RAG endpoints for airline policy queries.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from travel_assistant.app.error_handlers import register_error_handlers
from travel_assistant.app.routes import router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting Travel Assistant API...")
    yield
    # Shutdown
    logger.info("Shutting down Travel Assistant API...")


def create_app() -> FastAPI:
    """
    Creates and configures FastAPI application instance.

    Returns:
        Configured FastAPI application instance
    """
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Create FastAPI app with lifespan management
    fastapi_app = FastAPI(
        title="Travel Assistant AI",
        description="RAG-powered travel assistant for airline policy queries",
        version="1.0.0",
        lifespan=lifespan,
    )

    # Register error handlers
    register_error_handlers(fastapi_app)

    # Include routers
    fastapi_app.include_router(router)

    logger.info("FastAPI application configured successfully")
    return fastapi_app


# Create the app instance
app = create_app()
