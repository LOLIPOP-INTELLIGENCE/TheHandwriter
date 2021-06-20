from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

import time, os
import numpy as np
import cv2, pygame
import math, random
from PIL import Image

# Function to generate a handwritten image for a given word
def generate_word( _img_prev, _curr_word, _prev_exists, _num_spaces, _space_concat, _add_blank, _base_path ):

    #Random Set of Letters
    set = random.randint(2,3)
    #Random Error Character
    value_err = random.randint(1,11)

    #Retrieving path of revelant character
    characters     = list(_curr_word)
    character_first    = str( characters[0] )
    str_set         = str( set )

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

    fil_name        = '{}.jpg'

    if character_first.islower():      fil_name = fil_name.format( character_first + '_s' )
    elif character_first.isupper():    fil_name = fil_name.format( character_first.lower() + '_b' )
    elif character_first.isdigit():    fil_name = fil_name.format( character_first + '_d' )
    else:                           fil_name = fil_name.format( special_dct.get( character_first, 'blank1' ) + '_x' )


    #path holds the path to the first character in a word. If the word is Hello, 'path' is the path to 'H'
    path = _base_path + fil_name

    #creating the first image

    #To create more difference between characters, we add a rotation of the image by -10º to 10º
    degree=random.randint(-10,0)

    #Read image
    img = cv2.imread(path)

    #The below code converts all the black pixel values of that character to a standard value
    #For example consider an image has a black pixel of (0,0,0) and a black pixel of (30,30,30). For a standard look for the character,
    #we convert all the black pixels to a random value between 0-50
    hsv             = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    black_low       = np.array([0, 0, 0]) # anything from 0 to 50 is "black"
    black_high      = np.array([50, 50, 50])
    mask            = cv2.inRange(hsv, black_low, black_high)
    color_shade     = random.randint(0,50)
    img[mask > 0]   = (color_shade,color_shade,color_shade)

    #Adding a white padding of 3 pixels to the left and right of the image
    border = cv2.copyMakeBorder(
        img,
        top = 0, bottom = 0, left = 3, right = 3,
        borderType = cv2.BORDER_CONSTANT,
        value = (255, 255, 255)
    )

    #Adding the rotation
    im_pil = Image.fromarray(border)
    im_np = im_pil.rotate(degree,fillcolor='white')

    #Resizing the image and converting to numpy array so that we can concatenate images later on
    im_np = np.asarray(im_np)
    img = cv2.resize(im_np, (40, 114))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_np = np.array(img)
    final_img = img_np
    #doing the above for n-1 characters
    for i in range(1, len(characters)):
        value_err = random.randint(1, 11)
        value = random.randint(2, 3)

        degree          = random.randint(-10,0)
        characters_i    = str( characters[i] )
        str_val         = str( value )

        fil_name        = '{}.jpg'

        if characters_i.islower():      fil_name = fil_name.format( characters_i + '_s' )
        elif characters_i.isupper():    fil_name = fil_name.format( characters_i.lower() + '_b' )
        elif characters_i.isdigit():    fil_name = fil_name.format( characters_i + '_d' )
        else:                           fil_name = fil_name.format( special_dct.get( characters_i, 'blank1' ) + '_x' )

        path            = _base_path + fil_name

        img2 = cv2.imread(path)
        try:
            hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
        except:
            print(path)
        black_low = np.array([0, 0, 0])
        black_high = np.array([50, 50, 50])
        mask = cv2.inRange(hsv, black_low, black_high)
        color_shade = random.randint(0, 100)
        img2[mask > 0] = (color_shade, color_shade, color_shade)
        border = cv2.copyMakeBorder(
            img2,
            top=0,
            bottom=0,
            left=3,
            right=3,
            borderType=cv2.BORDER_CONSTANT,
            value=[255, 255, 255]
        )
        im_pil = Image.fromarray(border)
        im_np = im_pil.rotate(degree,fillcolor='white')
        im_np = np.asarray(im_np)
        img2 = cv2.resize(im_np, (40, 114))
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        img_np2 = np.array(img2)
        final_img = np.concatenate((img_np, img_np2), axis=1)
        img_np = final_img


    # This is there to add the image of previous words from _img_prev
    # Decide wether to add the previous part of the sentence to this word
    # For example, let the sentence be - "Hello there my name is Teddy"
    # After generating "Hello", k will be false since we don't have a previous image
    # After generating "there", k will be true and we will concatenate _img_prev to final_img
    # Similarly, after generating "my", k will be true and the image for "Hello there"(stored in _img_prev)
    # will be concatenated with final_img
    if (_prev_exists):
        final_img = np.concatenate((_img_prev, final_img), axis=1)
    if(_add_blank):
        final_img = generate_blank(final_img, _num_spaces, _space_concat,_base_path)

    return final_img
