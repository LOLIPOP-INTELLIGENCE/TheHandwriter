# 🖋️ Handwriting Generator FastAPI

A simple FastAPI application that replicates the exact functionality of your Lambda function - generates handwritten text images from typed input using pre-existing handwriting samples.

## ✨ What it does (exactly like the Lambda):

1. **Takes typed text** - Any text you want to convert
2. **Selects handwriting style** - Choose from 12 different handwriting styles
3. **Generates handwritten image** - Creates a realistic handwritten version
4. **Saves the image** - Stores it locally in the `static/` folder

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r simple_requirements.txt
```

### 2. Run the Server
```bash
python simple_main.py
```

### 3. Test It
```bash
python test_handwriting.py
```

## 📋 API Endpoints

### Generate Handwriting
```
GET /generate?typed=YOUR_TEXT&sel_hw=STYLE_NUMBER
```

**Example:**
```bash
curl "http://localhost:8000/generate?typed=Hello%20World&sel_hw=1"
```

**Response:**
```json
{
  "img_url": "/static/res_ABC123.jpg",
  "message": "Handwriting generated successfully", 
  "filename": "res_ABC123.jpg"
}
```

### List Available Styles
```
GET /handwriting-sets
```

**Response:**
```json
{
  "sets": [
    {"id": "1", "name": "Handwriting Style 1"},
    {"id": "2", "name": "Handwriting Style 2"},
    ...
  ]
}
```

### Get Generated Image
```
GET /static/{filename}
```

## 🎨 Available Handwriting Styles

- **Style 1-12**: Different handwriting styles from the original Lambda function
- Each style uses the same character mappings and generation logic as the Lambda

## 📁 Generated Images

- Images are saved in: `fastapi_app/static/`
- Access via: `http://localhost:8000/static/filename.jpg`
- Filenames use the same format as Lambda: `res_[unique_id].jpg`

## 🔧 How It Works

This FastAPI app uses the **exact same code** as your Lambda function:

1. `make_line_list()` - Splits text into proper lines
2. `generate_final_image()` - Creates handwritten characters
3. Uses the same character grid and image processing
4. Same rotation, padding, and styling logic
5. Saves images locally instead of uploading to S3

## 🧪 Testing

Run the test script to see it in action:

```bash
python test_handwriting.py
```

This will:
- ✅ Check API health
- ✅ List all handwriting styles  
- ✅ Generate sample handwritten texts
- ✅ Save multiple image examples

## 🌐 Interactive Docs

Visit `http://localhost:8000/docs` for interactive API documentation with Swagger UI.

---

**That's it!** This is your Lambda function running locally with FastAPI - same functionality, no external dependencies! 🎉 