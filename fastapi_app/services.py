import base64
import requests
import logging
from typing import Dict, Any, List
from fastapi import HTTPException
from config import settings
import time
import hashlib
import asyncio
import os
from datetime import datetime
import random

logger = logging.getLogger(__name__)

class HandwritingService:
    """Service class for handwriting-specific processing"""
    
    @staticmethod
    def get_default_handwriting_samples() -> List[Dict[str, str]]:
        """Get default handwriting samples for testing"""
        return [
            {
                "name": "Sample 1 - Cursive",
                "description": "Beautiful cursive handwriting sample",
                "style": "cursive",
                "sample_text": "The quick brown fox jumps over the lazy dog"
            },
            {
                "name": "Sample 2 - Print",
                "description": "Clear print handwriting sample",
                "style": "print",
                "sample_text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit"
            },
            {
                "name": "Sample 3 - Mixed",
                "description": "Mixed style handwriting sample",
                "style": "mixed",
                "sample_text": "Python FastAPI makes building APIs incredibly easy"
            }
        ]
    
    @staticmethod
    async def analyze_handwriting(base64_image: str, image_hash: str) -> Dict[str, Any]:
        """Analyze handwriting characteristics"""
        
        # Simulate handwriting analysis
        handwriting_features = {
            "text_detection": {
                "lines_detected": random.randint(3, 8),
                "words_detected": random.randint(15, 45),
                "characters_detected": random.randint(80, 200)
            },
            "style_analysis": {
                "writing_style": random.choice(["cursive", "print", "mixed"]),
                "slant_angle": round(random.uniform(-15, 15), 2),
                "letter_spacing": random.choice(["tight", "normal", "wide"]),
                "line_spacing": random.choice(["close", "normal", "wide"])
            },
            "quality_metrics": {
                "legibility_score": round(random.uniform(0.7, 0.95), 2),
                "consistency_score": round(random.uniform(0.6, 0.9), 2),
                "neatness_score": round(random.uniform(0.65, 0.9), 2)
            },
            "extracted_text": random.choice([
                "The quick brown fox jumps over the lazy dog",
                "Lorem ipsum dolor sit amet consectetur",
                "Python FastAPI handwriting analysis",
                "Sample handwritten text for processing"
            ])
        }
        
        return handwriting_features

class ImageService:
    """Service class for handling image processing operations"""
    
    @staticmethod
    async def encode_image_to_base64(image_content: bytes) -> str:
        """
        Encode image content to base64 string
        """
        try:
            return base64.b64encode(image_content).decode()
        except Exception as e:
            logger.error(f"Error encoding image to base64: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to encode image")
    
    @staticmethod
    async def save_processed_image(base64_image: str, filename: str = None) -> str:
        """Save processed image to disk"""
        try:
            # Create output directory if it doesn't exist
            output_dir = "processed_images"
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate filename if not provided
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"handwriting_{timestamp}.jpg"
            
            # Decode base64 and save
            image_data = base64.b64decode(base64_image)
            file_path = os.path.join(output_dir, filename)
            
            with open(file_path, 'wb') as f:
                f.write(image_data)
            
            logger.info(f"Image saved to: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Error saving image: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to save image")
    
    @staticmethod
    async def send_to_lambda(payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process image locally with handwriting analysis
        This simulates handwriting recognition processing
        """
        try:
            logger.info("Processing handwriting image locally")
            
            # Simulate processing time
            await asyncio.sleep(settings.simulate_processing_delay)
            
            # Get image data
            base64_image = payload.get("upl_hw", "")
            
            # Create a hash of the image for identification
            image_hash = hashlib.md5(base64_image.encode()).hexdigest()[:8]
            
            # Simulate image analysis
            image_size = len(base64_image)
            
            # Get handwriting analysis
            handwriting_analysis = await HandwritingService.analyze_handwriting(base64_image, image_hash)
            
            # Save the processed image
            try:
                saved_path = await ImageService.save_processed_image(base64_image, f"handwriting_{image_hash}.jpg")
            except:
                saved_path = "Failed to save image"
            
            # Mock response with handwriting-specific results
            mock_response = {
                "processed": True,
                "timestamp": time.time(),
                "image_info": {
                    "hash": image_hash,
                    "base64_length": image_size,
                    "estimated_size_kb": round(image_size * 0.75 / 1024, 2),
                    "saved_path": saved_path
                },
                "handwriting_analysis": handwriting_analysis,
                "processing_results": {
                    "status": "completed",
                    "processing_time_ms": int(settings.simulate_processing_delay * 1000),
                    "features_detected": ["text_lines", "character_boundaries", "handwriting_style"],
                    "confidence_score": handwriting_analysis["quality_metrics"]["legibility_score"]
                },
                "message": "Handwriting processed successfully (local simulation)"
            }
            
            logger.info(f"Handwriting processing completed for image hash: {image_hash}")
            return mock_response
                
        except Exception as e:
            logger.error(f"Error in local handwriting processing: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error processing handwriting locally: {str(e)}"
            )

class ValidationService:
    """Service class for input validation"""
    
    @staticmethod
    def validate_file_type(content_type: str) -> bool:
        """
        Validate if the file type is allowed
        """
        return content_type in settings.allowed_file_types
    
    @staticmethod
    def validate_file_size(file_size: int) -> bool:
        """
        Validate if the file size is within limits
        """
        return file_size <= settings.max_file_size 