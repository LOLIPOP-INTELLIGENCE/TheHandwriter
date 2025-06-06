# Local FastAPI Image Processing API

A clean, modular FastAPI application for processing images locally without external dependencies.

## Features

- 🚀 **FastAPI Framework** - Modern, fast web framework for building APIs
- 📁 **File Upload Support** - Direct image file uploads with validation
- 🔒 **Input Validation** - File type and size validation
- 📊 **Base64 Processing** - Direct base64 image processing endpoint
- 🔧 **Modular Architecture** - Clean separation of concerns
- 📖 **Auto-Generated Docs** - Interactive API documentation with Swagger UI
- 🚨 **Error Handling** - Comprehensive error handling and logging
- ⚙️ **Configuration Management** - Environment-based configuration
- 🏠 **Fully Local** - No external API calls or dependencies

## API Endpoints

### Health Check
- `GET /` - Basic health check
- `GET /health` - Detailed health status

### Image Processing
- `POST /upload-image` - Upload and process image files locally
- `POST /process-base64` - Process base64 encoded images locally

## Quick Start

### 1. Install Dependencies
```bash
cd fastapi_app
pip install -r requirements.txt
```

### 2. Run the Application
```bash
# Option 1: Using the run script
python run.py

# Option 2: Using uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Access the API
- **API Base URL**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Configuration

The application uses environment-based configuration. You can create a `.env` file to override default settings:

```env
HOST=0.0.0.0
PORT=8000
MAX_FILE_SIZE=10485760
SIMULATE_PROCESSING_DELAY=0.1
```

## Usage Examples

### Upload Image File
```bash
curl -X POST "http://localhost:8000/upload-image" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@your-image.jpg"
```

### Process Base64 Image
```bash
curl -X POST "http://localhost:8000/process-base64" \
     -H "accept: application/json" \
     -H "Content-Type: application/json" \
     -d '{"upl_hw": "base64-encoded-image-data"}'
```

## Local Processing

This application processes images entirely locally and returns mock analysis results including:

- Image hash for identification
- File size analysis
- Simulated feature detection (edges, text regions, handwriting)
- Processing confidence scores
- Timestamp and processing metadata

**No external API calls are made** - everything runs on your local machine.

## Project Structure

```
fastapi_app/
├── __init__.py          # Package initialization
├── main.py              # FastAPI application and routes
├── config.py            # Configuration management
├── models.py            # Pydantic models for request/response
├── services.py          # Business logic and local processing
├── requirements.txt     # Python dependencies
├── run.py              # Application runner script
├── test_client.py      # Test client for API testing
└── README.md           # This file
```

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- BMP (.bmp)

## File Size Limits

- Maximum file size: 10MB (configurable)
- Files larger than the limit will be rejected with a 413 error

## Error Handling

The API provides comprehensive error handling with appropriate HTTP status codes:

- `400` - Bad Request (invalid file type, malformed data)
- `413` - Payload Too Large (file size exceeds limit)
- `500` - Internal Server Error (processing errors)

## Development

### Running in Development Mode
```bash
# With auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Testing the API
Use the interactive documentation at http://localhost:8000/docs to test endpoints directly in your browser, or run the test client:

```bash
python test_client.py
```

## Architecture

The application follows a clean, modular architecture:

- **main.py**: FastAPI application setup and route definitions
- **config.py**: Centralized configuration management
- **models.py**: Pydantic models for data validation
- **services.py**: Business logic and local image processing
- **Separation of Concerns**: Each module has a specific responsibility

This architecture makes the code maintainable, testable, and easy to extend while keeping everything local and self-contained. 