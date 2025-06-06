#!/usr/bin/env python3
"""
FastAPI Application Runner

Run this script to start the local FastAPI application server.
"""

import uvicorn
from config import settings

if __name__ == "__main__":
    print(f"Starting {settings.api_title} v{settings.api_version}")
    print(f"Server will run at: http://{settings.host}:{settings.port}")
    print(f"API docs available at: http://{settings.host}:{settings.port}/docs")
    print("🏠 Running in LOCAL MODE - no external Lambda calls will be made")
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True,  # Enable auto-reload in development
        log_level="info"
    ) 