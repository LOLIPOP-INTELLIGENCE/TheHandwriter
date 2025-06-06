from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class Base64ImagePayload(BaseModel):
    """Model for base64 image payload"""
    upl_hw: str = Field(..., description="Base64 encoded image data")

class ImageResponse(BaseModel):
    """Standard response model for image operations"""
    status: str = Field(..., description="Status of the operation")
    message: str = Field(..., description="Human readable message")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data from Lambda")

class HealthResponse(BaseModel):
    """Health check response model"""
    message: str = Field(..., description="Health status message")
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error type")
    detail: str = Field(..., description="Error details")
    status_code: int = Field(..., description="HTTP status code") 