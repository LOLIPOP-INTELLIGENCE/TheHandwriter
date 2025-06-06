#!/usr/bin/env python3
"""
Test script for the Handwriting FastAPI application
"""

import requests
import time

# API configuration
API_BASE_URL = "http://localhost:8000"

def test_handwriting_sets():
    """Test getting available handwriting sets"""
    print("🎨 Testing handwriting sets...")
    try:
        response = requests.get(f"{API_BASE_URL}/handwriting-sets")
        response.raise_for_status()
        result = response.json()
        
        print(f"✅ Found {len(result['sets'])} handwriting sets:")
        for style in result['sets']:
            print(f"   - Style {style['id']}: {style['name']}")
        return result['sets']
        
    except Exception as e:
        print(f"❌ Error getting handwriting sets: {e}")
        return []

def test_generate_handwriting(text, style_id):
    """Test generating handwritten text"""
    print(f"\n✍️  Generating handwriting with style {style_id}...")
    print(f"   Text: '{text}'")
    
    try:
        params = {
            "typed": text,
            "sel_hw": style_id
        }
        response = requests.get(f"{API_BASE_URL}/generate", params=params)
        response.raise_for_status()
        result = response.json()
        
        print(f"✅ {result['message']}")
        print(f"   Image URL: {result['img_url']}")
        print(f"   Filename: {result['filename']}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error generating handwriting: {e}")
        return None

def main():
    """Run handwriting tests"""
    print("🚀 Testing Handwriting FastAPI Application\n")
    
    # Test health
    try:
        response = requests.get(f"{API_BASE_URL}/")
        print(f"✅ API Health: {response.json()['message']}\n")
    except:
        print("❌ API is not running. Please start the server first with: python simple_main.py")
        return
    
    # Test handwriting sets
    sets = test_handwriting_sets()
    if not sets:
        return
    
    # Test samples
    test_texts = [
        "Hello World! This is a test.",
        "The quick brown fox jumps over the lazy dog.",
        "Python FastAPI makes building APIs incredibly easy and fun!",
        "1234567890 ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz",
        "Special characters: !@#$%^&*()[]{}.,?;:"
    ]
    
    # Test with different styles
    test_styles = ["1", "3", "7", "10"]
    
    print(f"\n🧪 Testing handwriting generation...")
    
    for i, text in enumerate(test_texts[:3]):  # Test first 3 texts
        style = test_styles[i % len(test_styles)]
        result = test_generate_handwriting(text, style)
        if result:
            time.sleep(0.5)  # Small delay between requests
    
    print(f"\n🏁 Testing completed!")
    print(f"📁 Generated images are saved in: fastapi_app/static/")
    print(f"🌐 You can also access them via: {API_BASE_URL}/static/[filename]")
    print(f"📖 API docs available at: {API_BASE_URL}/docs")

if __name__ == "__main__":
    main() 