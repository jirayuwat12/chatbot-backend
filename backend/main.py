#!/usr/bin/env python3
"""
Main application file for the Bot Contact Point API.

This module initializes the FastAPI application with all necessary middleware,
configurations, and includes all API routers from the application.
"""
import asyncio
from contextlib import asynccontextmanager
from typing import Any, Dict

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Load environment variables from .env file
load_dotenv()

# Create FastAPI app instance with metadata for documentation
app = FastAPI(
    title="Bot Contact Point API",
    description="API for managing bot communications and interactions",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify actual origins instead of "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", status_code=status.HTTP_200_OK, tags=["Health"])
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint to verify the API is running.

    Returns:
        Dict[str, Any]: A dictionary containing status information
    """
    return {
        "status": "healthy",
        "message": "API is running",
        "service": "bot_contact_point",
        "version": "0.1.0",
    }


@app.get("/", status_code=status.HTTP_200_OK, tags=["Root"])
async def root() -> JSONResponse:
    """
    Root endpoint that redirects to the API documentation.

    Returns:
        JSONResponse: A response with welcome message and links to documentation
    """
    return JSONResponse(
        content={
            "message": "Welcome to Bot Contact Point API",
            "documentation": "/docs",
            "alternative_documentation": "/redoc",
        }
    )


if __name__ == "__main__":
    # Run the application with uvicorn when this file is executed directly
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
