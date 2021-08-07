from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

import time, os
import numpy as np
import cv2, pygame
import math, random
from PIL import Image

# Maximum number of characters per line
line_char_limit = 60

# Utility function to shorten a large number into a unique ID
def to_id( _num, _base = 64 ):

    if _num <= 0: return '0'

    charset = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_#'
    res     = ''

    while _num:
        rem     = _num % _base
        _num    //= _base
        res     += charset[rem]

    # return res[::-1]
    return res

# Function to resize the image to constant width
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

    name_lst = [['1_d0', '2_d0', '3_d0', '4_d0', '5_d0', '6_d0', '7_d0', '8_d0', '9_d0', '0_d0', 'a_s0', 'b_s0', 'c_s0', 'd_s0', 'e_s0', 'f_s0', 'g_s0', 'h_s0', 'i_s0', 'j_s0', 'k_s0', 'l_s0'],
                ['m_s0', 'n_s0', 'o_s0', 'p_s0', 'q_s0', 'r_s0', 's_s0', 't_s0', 'u_s0', 'v_s0', 'w_s0', 'x_s0', 'y_s0', 'z_s0', 'a_b0', 'b_b0', 'c_b0', 'd_b0', 'e_b0', 'f_b0', 'g_b0', 'h_b0'],
                ['i_b0', 'j_b0', 'k_b0', 'l_b0', 'm_b0', 'n_b0', 'o_b0', 'p_b0', 'q_b0', 'r_b0', 's_b0', 't_b0', 'u_b0', 'v_b0', 'w_b0', 'x_b0', 'y_b0', 'z_b0', 'dot_x0', 'comma_x0', 'question_x0', 'exclam_x0'],
                ['openb_x0', 'closeb_x0', 'openc_x0', 'closec_x0', 'opens_x0', 'closes_x0', 'plus_x0', 'minus_x0', 'multiply_x0', 'divide_x0', 'frontslash_x0', 'backslash_x0', 'lessthan_x0', 'morethan_x0', 'equals_x0', 'percent_x0', 'at_x0', 'squote_x0', 'dquote_x0', 'colon_x0', 'scolon_x0', 'and_x0'],
                ['1_d1', '2_d1', '3_d1', '4_d1', '5_d1', '6_d1', '7_d1', '8_d1', '9_d1', '0_d1', 'a_s1', 'b_s1', 'c_s1', 'd_s1', 'e_s1', 'f_s1', 'g_s1', 'h_s1', 'i_s1', 'j_s1', 'k_s1', 'l_s1'],
                ['m_s1', 'n_s1', 'o_s1', 'p_s1', 'q_s1', 'r_s1', 's_s1', 't_s1', 'u_s1', 'v_s1', 'w_s1', 'x_s1', 'y_s1', 'z_s1', 'a_b1', 'b_b1', 'c_b1', 'd_b1', 'e_b1', 'f_b1', 'g_b1', 'h_b1'],
                ['i_b1', 'j_b1', 'k_b1', 'l_b1', 'm_b1', 'n_b1', 'o_b1', 'p_b1', 'q_b1', 'r_b1', 's_b1', 't_b1', 'u_b1', 'v_b1', 'w_b1', 'x_b1', 'y_b1', 'z_b1', 'dot_x1', 'comma_x1', 'question_x1', 'exclam_x1'],
                ['openb_x1', 'closeb_x1', 'openc_x1', 'closec_x1', 'opens_x1', 'closes_x1', 'plus_x1', 'minus_x1', 'multiply_x1', 'divide_x1', 'frontslash_x1', 'backslash_x1', 'lessthan_x1', 'morethan_x1', 'equals_x1', 'percent_x1', 'at_x1', 'squote_x1', 'dquote_x1', 'colon_x1', 'scolon_x1', 'and_x1'],
                ['1_d2', '2_d2', '3_d2', '4_d2', '5_d2', '6_d2', '7_d2', '8_d2', '9_d2', '0_d2', 'a_s2', 'b_s2', 'c_s2', 'd_s2', 'e_s2', 'f_s2', 'g_s2', 'h_s2', 'i_s2', 'j_s2', 'k_s2', 'l_s2'],
                ['m_s2', 'n_s2', 'o_s2', 'p_s2', 'q_s2', 'r_s2', 's_s2', 't_s2', 'u_s2', 'v_s2', 'w_s2', 'x_s2', 'y_s2', 'z_s2', 'a_b2', 'b_b2', 'c_b2', 'd_b2', 'e_b2', 'f_b2', 'g_b2', 'h_b2'],
                ['i_b2', 'j_b2', 'k_b2', 'l_b2', 'm_b2', 'n_b2', 'o_b2', 'p_b2', 'q_b2', 'r_b2', 's_b2', 't_b2', 'u_b2', 'v_b2', 'w_b2', 'x_b2', 'y_b2', 'z_b2', 'dot_x2', 'comma_x2', 'question_x2', 'exclam_x2'],
                ['openb_x2', 'closeb_x2', 'openc_x2', 'closec_x2', 'opens_x2', 'closes_x2', 'plus_x2', 'minus_x2', 'multiply_x2', 'divide_x2', 'frontslash_x2', 'backslash_x2', 'lessthan_x2', 'morethan_x2', 'equals_x2', 'percent_x2', 'at_x2', 'squote_x2', 'dquote_x2', 'colon_x2', 'scolon_x2', 'and_x2']]

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

            cropped_img = crop_img( image, x+3, y+3, w-6, h-6 )

            if i >= 4:
                check_img   = crop_img( img_bin, x+3, y+3, w-6, h-6 )

                total_px = (w-6) * (h-6)
                white_px = cv2.countNonZero( check_img )

                if (total_px - white_px) < px_thresh:
                    cropped_img = cv2.imread( '{}/{}.jpg'.format( _final_path, name_lst[i - 4][j] ) )

            cv2.imwrite( '{}/{}.jpg'.format( _final_path, name_lst[i][j] ), cropped_img )
# Lambda function to generate spaces
generate_blank = lambda _num_spaces : np.ones( [100, 40 * _num_spaces] ) * 255

# Function to generate final words from raw input text
def make_line_list( _inp ):

    lines = []
    raw_lines = _inp.strip().split( '\r\n' )

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

# Generates the final image using the words as input
def generate_image( _words, _base_path ):

    special_dct     =   {'.':'dot_x',
                        ',':'comma_x',
                        '?':'question_x',
                        '!':'exclam_x',
                        '(':'openb_x',
                        ')':'closeb_x',
                        '{':'openc_x',
                        '}':'closec_x',
                        '[':'opens_x',
                        ']':'closes_x',
                        '+':'plus_x',
                        '-':'minus_x',
                        '*':'multiply_x',
                        'div':'divide_x',
                        '/':'frontslash_x',
                        '\\':'backslash_x',
                        '<':'lessthan_x',
                        '>':'morethan_x',
                        '=':'equals_x',
                        '%':'percent_x',
                        '@':'at_x',
                        '\'':'squote_x',
                        '"':'dquote_x',
                        ':':'colon_x',
                        ';':'scolon_x',
                        '&':'and_x',
                        '\n':'blank2',
                        '~':'error'
                        }

    #! Preload images by using buffer (cache)

    # Function to generate a handwritten image for a given word
    def generate_word( _img_prev, _curr_word, _num_spaces, _rot_rng = (-8, 3), _black_thresh = 50, _hor_pad = 0, _ver_pad = 0 ):

        #Retrieving path of revelant character
        characters  = list(_curr_word )
        # character_first     = str( characters[0] )

        img         = None

        for i in range( len( characters ) ):

            characters_i    = str( characters[i] )

            fil_name        = '{}' + str(np.random.randint(0,3)) + '.jpg'

            if characters_i.islower():      fil_name = fil_name.format( characters_i + '_s' )
            elif characters_i.isupper():    fil_name = fil_name.format( characters_i.lower() + '_b' )
            elif characters_i.isdigit():    fil_name = fil_name.format( characters_i + '_d' )
            else:                           fil_name = fil_name.format( special_dct.get( characters_i, 'blank1_x' ) )


            path            = _base_path + fil_name

            if(os.path.isfile(path)):
                img2            = cv2.cvtColor( cv2.imread( path ), cv2.COLOR_BGR2GRAY )

                mask            = cv2.inRange( img2, 0, _black_thresh )
                img2[mask > 0]  = random.randint( 0, _black_thresh )

                border          = cv2.copyMakeBorder(
                    img2,
                    top = _ver_pad, bottom = _ver_pad, left = _hor_pad, right = _hor_pad,
                    borderType = cv2.BORDER_CONSTANT,
                    value = (255,) * 3
                )

                im_pil          = Image.fromarray( border )
                im_np           = np.asarray( im_pil.rotate( random.randint( _rot_rng[0], _rot_rng[1] ), fillcolor = 'white' ) )
                img2            = cv2.resize( im_np, (40, 100) )
            else:
                img2            = generate_blank(1)
            img             = np.concatenate( (img, img2), axis = 1 ) if img is not None else img2

        if _img_prev is not None:
            final_img = np.concatenate( (_img_prev, img), axis = 1 )

        if _num_spaces:
            final_img = np.concatenate( (final_img, generate_blank( _num_spaces )), axis = 1 )

        return final_img

    # list of sentence images
    sentences       = []

    word_num        = 0
    max_words       = len( _words )
    while word_num < max_words:

        # maximum number of characters in a line
        max_line_char   = 59
        line_output     = generate_blank( 1 )

        # Repeat max_line_char times
        while max_line_char > 0:

            curr_word = _words[word_num]
            curr_len = len( curr_word )

            # LF character
            if _words[word_num] == '\n':

                # line_output = generate_blank( line_output, max_line_char )
                line_output = np.concatenate( (line_output, generate_blank( max_line_char )), axis = 1 )
                word_num += 1
                break

            # Regular word
            else:

                if curr_len >= 60:
                    curr_word, next_word = curr_word[0:59], curr_word[59:]
                    curr_len = len( curr_word )

                    _words.insert( word_num + 1, next_word )
                    max_words += 1
                    # print(_words)

                if max_line_char >= curr_len:

                    # Number of characters we need to add to the right in case this is the final word
                    right_pad = min( 2, max_line_char - curr_len )
                    line_output = generate_word( line_output, curr_word, right_pad )

                    # Subtracting the length of the word and the number of spaces added(t) from k\
                    max_line_char -= curr_len + right_pad
                    word_num += 1

                    if word_num > max_words:
                        if max_line_char:
                            line_output = np.concatenate( (line_output, generate_blank( max_line_char )), axis = 1 )
                        break

                else:

                    line_output = np.concatenate( (line_output, generate_blank( max_line_char )), axis = 1 )
                    break

        # Sentences hols all the sentences. line_output is the output for that line
        sentences.append( line_output )

    # for sentence in sentences:
        # print( np.size( sentence, 0 ), np.size( sentence, 1 ) )

    # Concatenatig all sentences to produce the final image
    final_output = sentences[0]
    # print(final_output.shape)
    for i in range(1, len(sentences)):
        # print(sentences[i].shape)
        final_output = np.concatenate((final_output, sentences[i]), axis = 0)

    # Adding a border for the page
    border = cv2.copyMakeBorder(
        final_output,
        top=120,
        bottom=40,
        left=100,
        right=30,
        borderType=cv2.BORDER_CONSTANT,
        value=[255,255,255]
    )

    white_lo        = 200
    white_hi        = 255

    mask            = cv2.inRange( border, white_lo, white_hi )
    border[mask > 0]= 255

    return border

def add( request ):
    request.session["txt"] = request.GET["text"]
    return render( request, "hm.html" )

def upload( request ):

    if request.method == "POST":

        # Get the file, input text and reference to filesystem object
        if "txt" not in request.session:
            res_path    = "static/default.jpg"
        else:
            inp_text    = request.session["txt"]

            myfile      = request.FILES["myfile"]
            fs          = FileSystemStorage()

            # Get the current time and convert it to an ID
            cur_time    = to_id( time.time_ns() )

            # Relative paths to the scan folder, submission, processed submission and result
            dir_path    = "media/AllHandwritings/scan_{}".format( cur_time )
            sub_path    = dir_path + "/submission.jpg"
            pro_path    = dir_path + "/processed_submission.jpg"
            res_path    = "static/res_{}.jpg".format( cur_time )

            # Create directory and save submission
            os.mkdir( dir_path )
            filename    = fs.save( "AllHandwritings/scan_{}/submission.jpg".format( cur_time ), myfile )

            # Preprocess submission and detect boxes
            preprocess( sub_path, pro_path )
            detect_box( pro_path, dir_path )

            # Generate handwritten image
            final_text  = make_words_final( inp_text )
            img         = generate_image( final_text, dir_path + '/' )
            cv2.imwrite( res_path, img )

            fs.url( filename )

        return render( request, 'r.html', {'image':res_path} )

def hx( request, _x ):

    # Get input text and paths to resultant image, input set
    if "txt" not in request.session:
        res_path    = "static/default.jpg"
    else:
        inp_text    = request.session["txt"]

        set_path    = "media/DisplayedHandwritings/set_{}/".format( _x )
        res_path    = "static/res_{}.jpg".format( to_id( time.time_ns() ) )

        final_text  = make_words_final( inp_text )
        img         = generate_image( final_text, set_path )
        cv2.imwrite( res_path, img )

    return render( request, 'r.html', {'image': res_path} )