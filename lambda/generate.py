import time, os
import numpy as np
import cv2, pygame
import random
from PIL import Image
import pickle
import bz2
import boto3
from io import BytesIO
import requests

import base64

from pathlib import Path as PATH

# REPO_DIR        = str( PATH(__file__).resolve().parent.parent.parent )
static_path     = '/static/'
media_path      = os.environ['LAMBDA_TASK_ROOT'] + '/media/'

# Maximum number of characters per line
line_char_limit = 60

# Grid of character names in order of their appearanec in list
name_lst        =   [['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l'],
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

# utility function to crop out a part of an image using width and height
crop_img = lambda  _img, _x, _y, _w, _h: _img[_y:_y+_h , _x:_x+_w]

# Utility function to shorten a large number into a unique ID (number in base 62 reversed)
def to_id( _num, _base = 62 ):

    if _num <= 0: return '0'

    charset = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    res     = ''

    while _num:
        rem     = _num % _base
        _num    //= _base
        res     += charset[rem]

    return res

def preprocess( _path, _final_path ):

    # Load the image and get dinensions
    try:
        _surf           = pygame.image.load( _path )
    except:

        # -14 is to remove submission.jpg at the end
        os.remove( _path )
        os.rmdir( _path[:-14] )

        return None

    width, height   = list( _surf.get_size() ).copy()

    # Rotate the image if height > width (in portrait mode)
    if width < height:
        _surf           = pygame.transform.rotate( _surf, 90 )
        width, height   = height, width

    # Calculate new dimensions (width remains constant)
    new_width       = 1800
    new_height      = round( ( height * new_width ) / width )

    # Resize and save image
    _surf = pygame.transform.smoothscale( _surf, (new_width, new_height) )
    pygame.image.save( _surf, _final_path )

    # Delete original submission
    os.remove( _path )

# Function to go through image and find rects
def detect_box( _path, _final_path, _white_lo = 225 ):

    coords              = { name_lst[i][j]: [] for i in range( len( name_lst ) ) for j in range( len( name_lst[i] ) ) }

    # Utility function to get cropped image
    crop_img = lambda  _img, _x, _y, _w, _h: _img[_y:_y+_h , _x:_x+_w]

    # Load the image
    image               = cv2.imread( _path )
    line_min_width      = 38

    # Threshold pixel count for detecting empty cell
    px_thresh           = 64

    # Convert to grayscale and binarize
    gray_scale          = cv2.cvtColor( image, cv2.COLOR_BGR2GRAY )
    th1, img_bin        = cv2.threshold( gray_scale, 200, 255, cv2.THRESH_BINARY )

    # Remove non-essential details by kernelling the image
    kernal_h            = np.ones( (1, line_min_width), np.uint8 )
    kernal_v            = np.ones( (line_min_width, 1), np.uint8 )
    img_bin_h           = cv2.morphologyEx( ~img_bin, cv2.MORPH_OPEN, kernal_h )
    img_bin_v           = cv2.morphologyEx( ~img_bin, cv2.MORPH_OPEN, kernal_v )

    # Get the resultant or of the two kernelled images
    img_bin_final       = img_bin_h | img_bin_v
    final_kernel        = np.ones((9, 9), np.uint8)
    img_bin_final       = cv2.dilate( src = img_bin_final, kernel = final_kernel, iterations = 1 )

    # Get connected components and remove residual components
    ret, labels, stats, centroids = cv2.connectedComponentsWithStats( image = ~img_bin_final, connectivity = 8, ltype = cv2.CV_32S )
    stats = stats[2:]

    # Containers to store the bounding rects
    max_rows            = 22
    unfilt_lst          = []
    lst                 = [[] for i in range( max_rows )]

    # Go through stats and remove non-essential details, change order from col-first to row-first
    for x, y, w, h, area in stats: unfilt_lst.append([y, x, h, w])
    unfilt_lst.sort()

    # Process unfiltered list into rows and coloumns of rects and sort each row based on coloumn
    for row in range( len( unfilt_lst ) ):
        y, x, h, w = unfilt_lst[row]
        lst[ row // max_rows ].append([x, y, w, h])
    for i in range( max_rows ): lst[i].sort()

    # Crop and save each image with the correct name
    for i in range( len( name_lst ) ):
        for j in range( len( name_lst[i] ) ):

            x, y, w, h  = lst[i][j]
            char        = name_lst[i][j]
            coords[char].append( [x + 3, y + 3, w - 6, h - 6] )

            if i >= 4:
                check_img   = crop_img( img_bin, x + 3, y + 3, w - 6, h - 6 )

                total_px = (w - 6) * (h - 6)
                white_px = cv2.countNonZero( check_img )

                if (total_px - white_px) < px_thresh:
                    coords[char][-1] = coords[char][-2].copy()

    # File to output all coordinates
    fout                = bz2.BZ2File( _final_path + "/dat.pbz2", "w" )
    pickle.dump( coords, fout )
    fout.close()

# Function to generate final words from raw input text
def make_line_list( _inp ):

    lines = []
    raw_lines = _inp.strip().split( '\n' )

    for line in raw_lines:

        curr_len = len( line )

        if curr_len <= line_char_limit:
            diff = line_char_limit - curr_len
            lines.append( line + (' ' * diff) )

        elif curr_len > line_char_limit:

            #! todo
            last_space = line[:line_char_limit].rfind( ' ' )

            if last_space != -1:
                res = line[:last_space+1]
                rem = line[last_space+1:]

                diff = line_char_limit - (last_space + 1)
                res += ' ' * diff

            else:
                res = line[:line_char_limit]
                rem = line[line_char_limit:]

            lines.append( res )
            lines += make_line_list( rem )

    return lines

# Generates the final image using the preprocessed line as input
def generate_final_image( _lines, _base_path, _rot_rng = (-8, 3), _black_thresh = 50, _hor_pad = 0, _ver_pad = 0 ):

    buff        = {}

    fin         = bz2.BZ2File( "{}/{}".format( _base_path, "dat.pbz2" ), "r")
    coords      = pickle.load( fin )
    fin.close()

    submission  = cv2.imread( "{}/{}".format( _base_path, "processed_submission.jpg" ) )

    def get_img( char ):

        res = buff.get( char, None )

        # Image not in buffer
        if not res:

            res = coords.get( char, None )
            if not res:
                return None

            for i in range( 3 ):

                x, y, w, h  = res[i]
                res[i]      = cv2.cvtColor( crop_img( submission,  x, y, w, h ), cv2.COLOR_BGR2GRAY )
                mask        = cv2.inRange( res[i], 0, _black_thresh )

                res[i][mask > 0] = random.randint( 0, _black_thresh )

                res[i]      = cv2.copyMakeBorder(
                    res[i],
                    top     = _ver_pad,
                    bottom  = _ver_pad,
                    left    = _hor_pad,
                    right   = _hor_pad,
                    borderType = cv2.BORDER_CONSTANT,
                    value   = (255,) * 3
                )

            buff[char]      = res

        # Return image
        return res[random.randint( 0, 2 )]

    final_image = np.ones( [100 * len( _lines ), 40 * line_char_limit] ) * 255

    for row in range( len( _lines ) ):

        rcoor   = row * 100
        line    = _lines[row]

        for col in range( line_char_limit ):

            ccoor       = col * 40
            char        = line[col]

            border      = get_img( char )

            if border is None:
                continue

            char_img    = Image.fromarray( border )
            char_img    = np.asarray( char_img.rotate( random.randint( _rot_rng[0], _rot_rng[1] ), fillcolor = 'white' ) )
            char_img    = cv2.resize( char_img, (40, 100) )

            final_image[rcoor : rcoor + 100 , ccoor : ccoor + 40] = char_img

    white_lo    = 200
    white_hi    = 255
    mask        = cv2.inRange( final_image, white_lo, white_hi )

    final_image[mask > 0]   = 255

    border = cv2.copyMakeBorder(
        final_image,
        top     = 120,
        bottom  = 40,
        left    = 100,
        right   = 30,
        borderType = cv2.BORDER_CONSTANT,
        value = (255,) * 3
    )

    return border

def lambda_handler(event, context):

    s3 = boto3.client('s3', 
                      aws_access_key_id="AKIAQB2AUH6FWWNFCK63", 
                      aws_secret_access_key="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", 
                      region_name="ap-south-1"
                      )
    bucket_name = 'handwriter'
    
    # get the typed text
    inp_text    = event['queryStringParameters']['typed']
    upl_hw      = event['queryStringParameters']['upl-hw']
    sel_hw      = event['queryStringParameters']['sel-hw']

    # Get the current time and convert it to an ID
    cur_time    = to_id( time.time_ns() )

    # start building the set path (it will start from media path)
    set_path    = media_path

    if upl_hw != "-1":  

        s3_sub_path = "submission_{}.jpg".format(cur_time)

        response = requests.get(upl_hw)
        response.raise_for_status()  # This will raise an HTTPError if the response status code is 4XX or 5XX

        upl_hw = response.content

        # dir_path    = os.environ['LAMBDA_TASK_ROOT'] + '/tmp/' + "AllHandwritings/scan_{}".format( cur_time )
        dir_path    = '/tmp/' + "scan_{}".format( cur_time )

        sub_path    = dir_path + "/submission.jpg"
        pro_path    = dir_path + "/processed_submission.jpg"

        os.mkdir(dir_path)
        
        with open(sub_path, "wb") as f:
            f.write(upl_hw)

        try:
            preprocess( sub_path, pro_path )
            detect_box( pro_path, dir_path )
        except Exception as e:
            return {'error': str(e)}
        
        try:
            s3.put_object(
                Bucket=bucket_name,
                Key=s3_sub_path,  # Using the new S3 path here
                Body=upl_hw,
                ContentType='image/jpeg',
                ACL='public-read'
            )
        except Exception as e:
            return {'error': str(e)}          

        set_path    = '/tmp/' + "scan_{}".format( cur_time )
        # set_path    = os.environ['LAMBDA_TASK_ROOT'] + '/tmp/' + "AllHandwritings/scan_{}".format( cur_time )

    else:
        set_path    += "DisplayedHandwritings/set_{}/".format( sel_hw )

    res_suf     = "res_{}.jpg".format( cur_time )
    res_path    = static_path + res_suf

    final_text  = make_line_list( inp_text )
    print(set_path)
    img         = generate_final_image( final_text, set_path )

    is_success, buffer = cv2.imencode(".jpg", img)
    img_bytes = buffer.tobytes()    

    try:
        s3.put_object(
            Bucket=bucket_name,
            Key=res_suf,
            Body=img_bytes,
            ContentType='image/jpeg',
            ACL='public-read'
        )
        response = {
            "statusCode": 200,
            "body": "Image uploaded successfully"
        }
        return {'img_url' : f'https://handwriter.s3.ap-south-1.amazonaws.com/{res_suf}'}

    except Exception as e:
        response = {
            "statusCode": 500,
            "body": str(e)
        }
        return response