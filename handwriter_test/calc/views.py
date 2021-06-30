from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

import time, os
import numpy as np
import cv2, pygame
import math, random
from PIL import Image

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
    _surf           = pygame.image.load( _path )
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

# Function to go through image and find rects
def detect_box( _path, _final_path, _white_lo = 225 ):

    name_lst = [['1_d', '2_d', '3_d', '4_d', '5_d', '6_d', '7_d', '8_d', '9_d', '0_d', 'a_s', 'b_s', 'c_s', 'd_s', 'e_s', 'f_s', 'g_s', 'h_s', 'i_s', 'j_s', 'k_s', 'l_s'],
                ['m_s', 'n_s', 'o_s', 'p_s', 'q_s', 'r_s', 's_s', 't_s', 'u_s', 'v_s', 'w_s', 'x_s', 'y_s', 'z_s', 'A_b', 'B_b', 'C_b', 'D_b', 'E_b', 'F_b', 'G_b', 'H_b'],
                ['I_b', 'J_b', 'K_b', 'L_b', 'M_b', 'N_b', 'O_b', 'P_b', 'Q_b', 'R_b', 'S_b', 'T_b', 'U_b', 'V_b', 'W_b', 'X_b', 'Y_b', 'Z_b', 'dot_x', 'comma_x', 'question_x', 'exclam_x'],
                ['openb_x', 'closeb_x', 'openc_x', 'closec_x', 'opens_x', 'closes_x', 'plus_x', 'minus_x', 'multiply_x', 'divide_x', 'frontslash_x', 'backslash_x', 'lessthan_x', 'morethan_x', 'equals_x', 'percent_x', 'at_x', 'squote_x', 'dquote_x', 'colon_x', 'scolon_x', 'and_x']]

    # Utility function to get cropped image
    crop_img = lambda  _img, _x, _y, _w, _h: _img[_y:_y+_h , _x:_x+_w]

    # Load the image
    image               = cv2.imread( _path )
    line_min_width      = 38

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

            cv2.imwrite( '{}/{}.jpg'.format( _final_path, name_lst[i][j] ), cropped_img )
# Lambda function to generate spaces
generate_blank = lambda _num_spaces : np.ones( [114, 40 * _num_spaces] ) * 255

# Function to handwrite a given input string
def handwrite( _input_string, _base_path, _saved_path = None ):

    words_final = []
    lines       = _input_string.strip().split( '\r\n' )

    for line in lines:
        words_in_line   = line.split( ' ' )

        for word in words_in_line:
            if len( word ):
                words_final.append( word )

        words_final.append( '\n' )

    img         = generate_image( words_final, _base_path )

    if _saved_path:
        cv2.imwrite( _saved_path, img )
    return img

# Function to generate a handwritten image for a given word
def generate_word( _img_prev, _curr_word, _num_spaces, _base_path, _rot_rng = (-8, 3), _black_thresh = 50, _hor_pad = 3, _ver_pad = 0 ):

    #Retrieving path of revelant character
    characters  = list(_curr_word )
    # character_first     = str( characters[0] )

    special_dct     =   {'?':'question',
                        '!':'exclamation',
                        ',':'comma',
                        '.':'dot',
                        '/':'f_slash',
                        '/':'b_slash',
                        '(':'o_bracket',
                        '{':'o_curly',
                        '[':'o_square',
                        ')':'c_bracket',
                        '}':'c_curly',
                        ']':'c_square',
                        ':':'colon',
                        ';':'semicolon',
                        ' ':'blank2',
                        '\n':'blank2',
                        '~':'error'}

    img         = None

    for i in range( len( characters ) ):

        characters_i    = str( characters[i] )

        fil_name        = '{}.jpg'
        if characters_i.islower():      fil_name = fil_name.format( characters_i + '_s' )
        elif characters_i.isupper():    fil_name = fil_name.format( characters_i.lower() + '_b' )
        elif characters_i.isdigit():    fil_name = fil_name.format( characters_i + '_d' )
        else:                           fil_name = fil_name.format( special_dct.get( characters_i, 'blank1' ) + '_x' )

        path            = _base_path + fil_name
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
        img2            = cv2.resize( im_np, (40, 114) )
        img             = np.concatenate( (img, img2), axis = 1 ) if img is not None else img2

    if _img_prev is not None:
        final_img = np.concatenate( (_img_prev, img), axis = 1 )

    if _num_spaces:
        final_img = np.concatenate( (final_img, generate_blank( _num_spaces )), axis = 1 )

    return final_img

# Generates the final image using the words as input
def generate_image( _words, _base_path ):

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

                if max_line_char >= curr_len:

                    # Number of characters we need to add to the right in case this is the final word
                    # right_pad = int((max_line_char - curr_len) > 2) * 2
                    right_pad = min( 2, max_line_char - len( _words[word_num] ) )
                    line_output = generate_word( line_output, curr_word, right_pad, _base_path )

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

    for sentence in sentences:
        print( np.size( sentence, 0 ), np.size( sentence, 1 ) )

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

    path = _base_path + 'result.jpg'

    cv2.imwrite(path, border)

    return border

def add(request):
    request.session["txt"] = request.GET["text"]
    return render( request, "hm.html" )

def upload(request):

    if request.method == "POST":

        # Get the file, input text and reference to filesystem object
        myfile      = request.FILES["myfile"]
        inp_text    = request.session["txt"]
        fs          = FileSystemStorage()

        # Get the current time and convert it to an ID
        cur_time    = to_id( time.time_ns() )

        # Relative paths to the scan folder, submission, processed submission and result
        dir_path    = "media/AllHandwritings/scan_{}".format( cur_time )
        sub_path    = dir_path + "/submission.jpg"
        pro_path    = dir_path + "/processed_submission.jpg"
        res_path    = dir_path + "/result.jpg"

        # Create directory and save submission
        os.mkdir( dir_path )
        filename    = fs.save( "AllHandwritings/scan_{}/submission.jpg".format( cur_time ), myfile )

        # Preprocess submission and detect boxes
        preprocess( sub_path, pro_path )
        detect_box( pro_path, dir_path )

        # Generate handwritten image
        img         = handwrite( inp_text, dir_path + '/' )
        upload_url  = fs.url( filename )

        return render( request, 'r.html', {'image':res_path} )

def hx( request, _x ):

    # Get input text and paths to resultant image, input set
    inp_txt     = request.session["txt"]
    set_path    = "media/DisplayedHandwritings/set_{}/".format( _x )
    res_path    = "media/DisplayedHandwritings/res_imgs/res_{}.jpg".format( to_id( time.time_ns() ) )

    handwrite( inp_txt, set_path , res_path )

    return render( request, 'r.html', {'image': res_path} )