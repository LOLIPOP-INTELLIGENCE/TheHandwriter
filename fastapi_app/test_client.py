#!/usr/bin/env python3
"""
Test client for the FastAPI Image Processing API

This script demonstrates how to use the API programmatically.
"""

import requests
import base64
import json
from pathlib import Path

# API configuration
API_BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        response.raise_for_status()
        print(f"✅ Health check successful: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_file_upload(image_path: str):
    """Test file upload endpoint"""
    print(f"Testing file upload with {image_path}...")
    
    if not Path(image_path).exists():
        print(f"❌ Image file not found: {image_path}")
        return False
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': (Path(image_path).name, f, 'image/jpeg')}
            response = requests.post(f"{API_BASE_URL}/upload-image", files=files)
            response.raise_for_status()
            
        result = response.json()
        print(f"✅ File upload successful: {result['message']}")
        print(f"   Response data: {json.dumps(result.get('data', {}), indent=2)}")
        return True
        
    except Exception as e:
        print(f"❌ File upload failed: {e}")
        return False

def test_base64_processing(image_path: str):
    """Test base64 image processing endpoint"""
    print(f"Testing base64 processing with {image_path}...")
    
    if not Path(image_path).exists():
        print(f"❌ Image file not found: {image_path}")
        return False
    
    try:
        # Read and encode image
        with open(image_path, 'rb') as f:
            image_data = f.read()
            base64_image = base64.b64encode(image_data).decode()
        
        # Send to API
        payload = {"upl_hw": base64_image}
        response = requests.post(f"{API_BASE_URL}/process-base64", json=payload)
        response.raise_for_status()
        
        result = response.json()
        print(f"✅ Base64 processing successful: {result['message']}")
        print(f"   Response data: {json.dumps(result.get('data', {}), indent=2)}")
        return True
        
    except Exception as e:
        print(f"❌ Base64 processing failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting API tests...\n")
    
    # Test health check
    if not test_health_check():
        print("❌ API is not running. Please start the server first.")
        return
    
    print()
    
    # Look for test image
    test_image_path = "../test.jpg"  # Adjust path as needed
    
    if Path(test_image_path).exists():
        print(f"Using test image: {test_image_path}\n")
        
        # Test file upload
        test_file_upload(test_image_path)
        print()
        
        # Test base64 processing
        test_base64_processing(test_image_path)
        print()
    else:
        print(f"⚠️  Test image not found at {test_image_path}")
        print("   Please provide a test image or update the path in this script.")
    
    print("🏁 Tests completed!")

if __name__ == "__main__":
    main() 