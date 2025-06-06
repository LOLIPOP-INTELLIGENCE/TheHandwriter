from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import time, os
import numpy as np
import cv2
import random
from PIL import Image
import pickle
import bz2
from io import BytesIO
import requests
import base64
from pathlib import Path as PATH
import shutil

app = FastAPI(title="Handwriter API", description="Generate handwritten text from input", version="1.0.0")

# Configuration
static_path = './static/'
media_path = '../lambda/media/'
line_char_limit = 60

# Create directories
os.makedirs(static_path, exist_ok=True)
os.makedirs('./tmp/', exist_ok=True)

# Grid of character names in order of their appearance in list
name_lst = [['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l'],
            ['m', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
            ['I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '.', ',', '?', '!'],
            ['(', ')', '{', '}', '[', ']', '+', '-', '*', '÷', '/', '\\', '<', '>', '=', '%', '@', '\'', '"', ':', 's:', '&'],
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l'],
            ['m', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
            ['I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '.', ',', '?', '!'],
            ['(', ')', '{', '}', '[', ']', '+', '-', '*', '÷', '/', '\\', '<', '>', '=', '%', '@', '\'', '"', ':', 's:', '&'],
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l'],
            ['m', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
            ['I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '.', ',', '?', '!'],
            ['(', ')', '{', '}', '[', ']', '+', '-', '*', '÷', '/', '\\', '<', '>', '=', '%', '@', '\'', '"', ':', 's:', '&']]

# Utility functions from the Lambda
crop_img = lambda _img, _x, _y, _w, _h: _img[_y:_y+_h, _x:_x+_w]

def to_id(_num, _base=62):
    if _num <= 0: return '0'
    charset = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    res = ''
    while _num:
        rem = _num % _base
        _num //= _base
        res += charset[rem]
    return res

def make_line_list(_inp):
    lines = []
    raw_lines = _inp.strip().split('\n')
    
    for line in raw_lines:
        curr_len = len(line)
        
        if curr_len <= line_char_limit:
            diff = line_char_limit - curr_len
            lines.append(line + (' ' * diff))
        elif curr_len > line_char_limit:
            last_space = line[:line_char_limit].rfind(' ')
            
            if last_space != -1:
                res = line[:last_space+1]
                rem = line[last_space+1:]
                diff = line_char_limit - (last_space + 1)
                res += ' ' * diff
            else:
                res = line[:line_char_limit]
                rem = line[line_char_limit:]
            
            lines.append(res)
            lines += make_line_list(rem)
    
    return lines

def generate_final_image(_lines, _base_path, _rot_rng=(-8, 3), _black_thresh=50, _hor_pad=0, _ver_pad=0):
    buff = {}
    
    try:
        fin = bz2.BZ2File("{}/{}".format(_base_path, "dat.pbz2"), "r")
        coords = pickle.load(fin)
        fin.close()
    except:
        raise HTTPException(status_code=500, detail="Could not load handwriting data")
    
    try:
        submission = cv2.imread("{}/{}".format(_base_path, "processed_submission.jpg"))
    except:
        raise HTTPException(status_code=500, detail="Could not load handwriting image")

    def get_img(char):
        res = buff.get(char, None)
        
        if not res:
            res = coords.get(char, None)
            if not res:
                return None
            
            for i in range(3):
                x, y, w, h = res[i]
                res[i] = cv2.cvtColor(crop_img(submission, x, y, w, h), cv2.COLOR_BGR2GRAY)
                mask = cv2.inRange(res[i], 0, _black_thresh)
                res[i][mask > 0] = random.randint(0, _black_thresh)
                res[i] = cv2.copyMakeBorder(
                    res[i],
                    top=_ver_pad,
                    bottom=_ver_pad,
                    left=_hor_pad,
                    right=_hor_pad,
                    borderType=cv2.BORDER_CONSTANT,
                    value=(255,) * 3
                )
            buff[char] = res
        
        return res[random.randint(0, 2)]

    final_image = np.ones([100 * len(_lines), 40 * line_char_limit]) * 255
    
    for row in range(len(_lines)):
        rcoor = row * 100
        line = _lines[row]
        
        for col in range(line_char_limit):
            ccoor = col * 40
            char = line[col]
            border = get_img(char)
            
            if border is None:
                continue
            
            char_img = Image.fromarray(border)
            char_img = np.asarray(char_img.rotate(random.randint(_rot_rng[0], _rot_rng[1]), fillcolor='white'))
            char_img = cv2.resize(char_img, (40, 100))
            
            final_image[rcoor:rcoor + 100, ccoor:ccoor + 40] = char_img

    white_lo = 200
    white_hi = 255
    mask = cv2.inRange(final_image, white_lo, white_hi)
    final_image[mask > 0] = 255
    
    border = cv2.copyMakeBorder(
        final_image,
        top=120,
        bottom=40,
        left=100,
        right=30,
        borderType=cv2.BORDER_CONSTANT,
        value=(255,) * 3
    )
    
    return border

@app.get("/")
async def root():
    return {"message": "Handwriter API is running"}

@app.get("/generate")
async def generate_handwriting(typed: str, sel_hw: str = "1"):
    """
    Generate handwritten text image
    
    - **typed**: The text to convert to handwriting
    - **sel_hw**: Handwriting style set number (1-12)
    """
    try:
        # Get the current time and convert it to an ID
        cur_time = to_id(time.time_ns())
        
        # Set path to handwriting set
        set_path = media_path + "DisplayedHandwritings/set_{}/".format(sel_hw)
        
        # Check if handwriting set exists
        if not os.path.exists(set_path):
            raise HTTPException(status_code=404, detail=f"Handwriting set {sel_hw} not found")
        
        # Generate filename
        res_suf = "res_{}.jpg".format(cur_time)
        res_path = static_path + res_suf
        
        # Process text and generate image
        final_text = make_line_list(typed)
        img = generate_final_image(final_text, set_path)
        
        # Save image
        cv2.imwrite(res_path, img)
        
        return {
            "img_url": f"/static/{res_suf}",
            "message": "Handwriting generated successfully",
            "filename": res_suf
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/static/{filename}")
async def get_static_file(filename: str):
    """Serve generated images"""
    file_path = static_path + filename
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        raise HTTPException(status_code=404, detail="File not found")

@app.get("/handwriting-sets")
async def list_handwriting_sets():
    """List available handwriting sets"""
    sets_path = media_path + "DisplayedHandwritings/"
    if not os.path.exists(sets_path):
        return {"sets": [], "message": "No handwriting sets found"}
    
    sets = []
    for item in os.listdir(sets_path):
        if item.startswith("set_") and os.path.isdir(os.path.join(sets_path, item)):
            set_num = item.replace("set_", "")
            sets.append({"id": set_num, "name": f"Handwriting Style {set_num}"})
    
    return {"sets": sorted(sets, key=lambda x: int(x["id"])), "message": f"Found {len(sets)} handwriting sets"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 