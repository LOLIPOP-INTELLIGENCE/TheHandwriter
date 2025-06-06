import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    
    # API configuration
    api_title: str = "Local Image Processing API"
    api_description: str = "A local FastAPI application for processing images without external dependencies"
    api_version: str = "1.0.0"
    
    # Server configuration
    host: str = "0.0.0.0"
    port: int = 8000
    
    # File upload limits
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_file_types: list = ["image/jpeg", "image/jpg", "image/png", "image/gif", "image/bmp"]
    
    # Processing configuration
    simulate_processing_delay: float = 0.1  # seconds
    
    class Config:
        env_file = ".env"

# Create settings instance
settings = Settings() 