from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
import logging
from config import settings
from models import ImageResponse, Base64ImagePayload, HealthResponse
from services import ImageService, ValidationService, HandwritingService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version
)

@app.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint"""
    return HealthResponse(
        message="Local Handwriting Processing API is running",
        status="healthy",
        version=settings.api_version
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Detailed health check endpoint"""
    return HealthResponse(
        message="Service is healthy and ready to process handwriting images",
        status="healthy",
        version=settings.api_version
    )

@app.get("/handwriting/samples")
async def get_handwriting_samples():
    """
    Get default handwriting samples for testing
    
    Returns: List of available handwriting samples with descriptions
    """
    try:
        samples = HandwritingService.get_default_handwriting_samples()
        return {
            "status": "success",
            "message": "Default handwriting samples retrieved",
            "samples": samples,
            "count": len(samples)
        }
    except Exception as e:
        logger.error(f"Error getting handwriting samples: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get handwriting samples")

@app.post("/upload-handwriting", response_model=ImageResponse)
async def upload_handwriting_image(file: UploadFile = File(...)):
    """
    Upload a handwriting image file for analysis and processing
    
    - **file**: Handwriting image file to process (JPEG, PNG, GIF, BMP)
    - Returns: Detailed handwriting analysis and saved image path
    """
    try:
        # Validate file type
        if not ValidationService.validate_file_type(file.content_type):
            raise HTTPException(
                status_code=400,
                detail=f"File type {file.content_type} not allowed. Allowed types: {settings.allowed_file_types}"
            )
        
        # Read file content
        image_content = await file.read()
        
        # Validate file size
        if not ValidationService.validate_file_size(len(image_content)):
            raise HTTPException(
                status_code=413,
                detail=f"File size too large. Maximum size: {settings.max_file_size} bytes"
            )
        
        logger.info(f"Processing handwriting image: {file.filename}, size: {len(image_content)} bytes")
        
        # Encode to base64
        base64_image = await ImageService.encode_image_to_base64(image_content)
        
        # Prepare payload
        payload = {"upl_hw": base64_image}
        
        # Process handwriting
        response = await ImageService.send_to_lambda(payload)
        
        return ImageResponse(
            status="success",
            message=f"Handwriting image '{file.filename}' processed and saved successfully",
            data=response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing handwriting upload: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing handwriting: {str(e)}")

@app.post("/upload-image", response_model=ImageResponse)
async def upload_image(file: UploadFile = File(...)):
    """
    Upload an image file and send it for processing
    
    - **file**: Image file to process (JPEG, PNG, GIF, BMP)
    - Returns: Processing result
    """
    try:
        # Validate file type
        if not ValidationService.validate_file_type(file.content_type):
            raise HTTPException(
                status_code=400,
                detail=f"File type {file.content_type} not allowed. Allowed types: {settings.allowed_file_types}"
            )
        
        # Read file content
        image_content = await file.read()
        
        # Validate file size
        if not ValidationService.validate_file_size(len(image_content)):
            raise HTTPException(
                status_code=413,
                detail=f"File size too large. Maximum size: {settings.max_file_size} bytes"
            )
        
        logger.info(f"Processing image: {file.filename}, size: {len(image_content)} bytes")
        
        # Encode to base64
        base64_image = await ImageService.encode_image_to_base64(image_content)
        
        # Prepare payload
        payload = {"upl_hw": base64_image}
        
        # Send to Lambda
        response = await ImageService.send_to_lambda(payload)
        
        return ImageResponse(
            status="success",
            message=f"Image '{file.filename}' processed successfully",
            data=response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing image upload: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.post("/process-base64", response_model=ImageResponse)
async def process_base64_image(payload: Base64ImagePayload):
    """
    Process a base64 encoded image directly
    
    - **payload**: JSON object containing base64 encoded image in 'upl_hw' field
    - Returns: Processing result
    """
    try:
        logger.info(f"Processing base64 image, length: {len(payload.upl_hw)}")
        
        # Send to Lambda
        response = await ImageService.send_to_lambda(payload.dict())
        
        return ImageResponse(
            status="success",
            message="Base64 image processed successfully",
            data=response
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing base64 image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port) 