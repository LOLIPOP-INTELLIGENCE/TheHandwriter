from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

import time, os
import numpy as np
import cv2, pygame
import math, random
from PIL import Image

own_handwriting = lambda request : render( request, "io.html" )
home            = lambda request : render( request, "home.html" )

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
def detect_box( _path, _final_path ):

    name_lst = [['a_s', 'b_s', 'c_s', 'd_s', 'e_s', 'f_s', 'g_s', 'h_s', 'i_s', 'j_s', 'k_s', 'l_s', 'm_s', 'n_s', 'o_s', 'p_s', 'q_s', 'r_s', 's_s', 't_s'],
            ['u_s', 'v_s', 'w_s', 'x_s', 'y_s', 'z_s', 'a_b', 'b_b', 'c_b', 'd_b', 'e_b', 'f_b', 'g_b', 'h_b', 'i_b', 'j_b', 'k_b', 'l_b', 'm_b', 'n_b'],
            ['o_b', 'p_b', 'q_b', 'r_b', 's_b', 't_b', 'u_b', 'v_b', 'w_b', 'x_b', 'y_b', 'z_b', 'dot_x', 'comma_x', 'question_x', 'blank_x']]

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
    max_rows            = 20
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
            x, y, w, h = lst[i][j]
            cropped_img = crop_img( image, x+3, y+3, w-6, h-6 )
            cv2.imwrite( '{}\\{}.jpg'.format( _final_path, name_lst[i][j] ), cropped_img )

# Function to handwrite a given input string
def handwrite(input_string, _base_path):
    contents=input_string
    contents=contents.strip()

    # Splitting the input file by words - "word"
    words=contents.split(" ")

    num_words=len(words)
    i=0

    # Consider this input - ['mediators', 'are', '\\n\\n\\n\\n', 'seeking', 'to', 'cement']
    # The below while loop along with the try except is trying to convert "\\n\\n\\n\\n" to ['mediators', 'are', '\n', '\n', '\n', '\n', 'seeking', 'to', 'cement']
    # Reason to do this is because later in the program if the program finds a '\n' as a word, it will fill the current line with empty spaces
    while(i<num_words):
        if(words[i].startswith('\n') or words[i].startswith('\\n')):
            if(words[i].startswith('\n')):
                word_t=(words[i][1:])
            else:
                word_t=(words[i][2:])
            words.insert(i,'\n')
            words[i+1]=word_t
            num_words=num_words+1
        i=i+1

    try:
        while True:
            words.remove('')
    except ValueError:
        pass

    #generate random errors
    l=0
    pop=0

    # errors_for_number_for_words is the number of words for which the program adds one error
    # If it is 5 => For every 5 words there is 1 error
    errors_for_number_for_words=13

    # The below code adds an error character, a ~ to the begining of a word selected randomly with a frequency of errors_for_number_for_words
    randomlist = []
    if(((len(words))/errors_for_number_for_words)-3>=0):
        pop=int(((len(words))/errors_for_number_for_words)-3)
    for i in range(0,pop):
        n = random.randint(2, len(words) - 3)
        while(words[n]=='\n'):
            n = random.randint(2,len(words)-3)
        randomlist.append(n)
    for i in range(0,pop):
        word____err=words[randomlist[i]]
        word____err="~"+word____err
        words[randomlist[i]]=word____err

    return generate_image(words, _base_path)

# Function to generate a handwritten image for a given word
def generate_word(img_prev, word__k, prev_img_exists,N___K,K___K,add_blank, base_path):

    base_path = base_path

    #Random Set of Letters
    set = random.randint(2,3)
    #Random Error Character
    value_err = random.randint(1,11)

    #Retrieving path of revelant character
    characters     = list(word__k)
    character_first    = str( characters[0] )
    str_set         = str( set )

    special_dct     =   {'?':'question',
                        '!':'exclamation',
                        ',':'comma',
                        '.':'dot',
                        '/':'f_slash',
                        '\\':'b_slash',
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
    elif character_first.isupper():    fil_name = fil_name.format( character_first + '_b' )
    elif character_first.isdigit():    fil_name = fil_name.format( character_first + '_d' )
    else:                           fil_name = fil_name.format( special_dct.get( character_first, 'blank1' ) + '_x' )

    #path holds the path to the first character in a word. If the word is Hello, 'path' is the path to 'H'
    path = base_path + fil_name

    #creating the first image

    #To create more difference between characters, we add a rotation of the image by -10º to 10º
    degree=random.randint(-10,0)

    #Read image
    img = cv2.imread(path)

    #The below code converts all the black pixel values of that character to a standard value
    #For example consider an image has a black pixel of (0,0,0) and a black pixel of (30,30,30). For a standard look for the character,
    #we convert all the black pixels to a random value between 0-50
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    black_low = np.array([0, 0, 0])
    black_high = np.array([50, 50, 50])
    mask = cv2.inRange(hsv, black_low, black_high)
    color_shade=random.randint(0,50)
    img[mask > 0] = (color_shade,color_shade,color_shade)

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
        elif characters_i.isupper():    fil_name = fil_name.format( characters_i + '_b' )
        elif characters_i.isdigit():    fil_name = fil_name.format( characters_i + '_d' )
        else:                           fil_name = fil_name.format( special_dct.get( characters_i, 'blank1' ) + '_x' )

        path            = base_path + fil_name

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


    # This is there to add the image of previous words from img_prev
    # Decide wether to add the previous part of the sentence to this word
    # For example, let the sentence be - "Hello there my name is Teddy"
    # After generating "Hello", k will be false since we don't have a previous image
    # After generating "there", k will be true and we will concatenate img_prev to final_img
    # Similarly, after generating "my", k will be true and the image for "Hello there"(stored in img_prev)
    # will be concatenated with final_img
    if (prev_img_exists):
        final_img = np.concatenate((img_prev, final_img), axis=1)
    if(add_blank):
        final_img = generate_blank(final_img, N___K, K___K,base_path)

    return final_img

# Function to generate blanks
def generate_blank( _img_prev, _num_spaces, _prev_exists, _base_path ):

    # Return 1 previous image if number of spaces is 0
    if _num_spaces <= 0: return _img_prev

    # Load space texture amd prepare final image
    path        = _base_path + 'blank_x.jpg'
    spc         = np.array( cv2.resize( cv2.imread( path, 0 ), (40, 114) ) )
    final       = np.copy( spc )

    # Concatenate space texture until finished
    for i in range( _num_spaces - 1 ):
        final   = np.concatenate( (final, spc), axis = 1 )

    # If the previous image exists then concatenate it
    if _prev_exists:
        final   = np.concatenate( (_img_prev, final), axis = 1 )

    return final

def generate_image(words,_base_path):
    word_num=0
    #line output
    line_output=0
    #array of sentences
    sentences=[]

    # The below 2 variables are debug that will be printed out later
    MY_OUTPUT=''
    MY_SENTENCE_OUTPUT=[]
    while(word_num<len(words)):
        #Adding 60 characters in a line
        k=60

        # k>0 so that we don't overflow in a line
        while(k>0):
            try:
                # Handle separate case for \n as a word. Hence checking here first
                if(words[word_num]!='\n'):

                    # If we have not started with the line, ie 60 characters still remain
                    if(k==60):

                        # To make it look random, we generate either 1 blank space or 2 before starting with the word
                        # X-holds the number of spaces to be generated(either 1 or 2)
                        # Here img_prev_k is 0 because we don't have a previous image to concatenate
                        # N__k is X(the number of spaces to add)
                        # k__k is false because we are not concatenating the previous image
                        X=random.randint(1,2)
                        line_output=generate_blank(0,X,False,_base_path)

                        # From 60 characters, we remove X characters as we have added that many spaces
                        k=k-X

                        # Now we generate our first word
                        # f is 0
                        # k is true because we want to add the previous image(the initial blank space(s)) generated above
                        # N__K is 3 because we add 3 units of blank space characters
                        # K__K is true because when we call generate_blank() function inside the generate_word() function, we
                        # would have generated the word and hence we want the generate_blank() function to also concatenate the word
                        # add_blank is also true since we want 3 blank spaces
                        line_output = generate_word(img_prev=line_output, word__k=words[word_num], prev_img_exists=True, N___K=3, K___K=True, add_blank=True,base_path=_base_path)

                        #Debug
                        MY_OUTPUT = MY_OUTPUT + words[word_num] + '   '

                        # Remove the number of characters of word[f] and 3 spaces from k
                        k=k-(len(words[word_num])+3)

                        # Successfuly added the first word
                        word_num=word_num+1

                    # Now if we do not have 60 characters left in a line
                    else:

                        # Here we check if we can completely add the word in the given line
                        # For exmaple, If our sentence is - Hello there my name is bcdgdcdgchdghghcghjs
                        # Obviously bcdgdcdgchdghghcghjs cannot be added in the same line so the below condition checks for that
                        if(k-len(words[word_num])>=0):

                            # t tells us how many blank spaces we can add after adding our current word
                            # The standrad is 3 spaces but in the case that after adding the word, there is only 1 character left
                            # we take the minimum of 3 and k-len(words[f)
                            t=min(3,k-len(words[word_num]))

                            # Now we generate the word
                            # The parameters mean the same as they did above when k was == 60
                            line_output = generate_word(img_prev=line_output, word__k=words[word_num], prev_img_exists=True, N___K=t, K___K=True, add_blank=True,base_path=_base_path)

                            # Debug variable
                            MY_OUTPUT=MY_OUTPUT+words[word_num]
                            MY_OUTPUT = MY_OUTPUT.ljust(t + len(MY_OUTPUT), ' ')

                            # Subtracting the length of the word and the number of spaces added(t) from k\
                            k=k-(len(words[word_num])+t)

                            # Successfuly added the word, and increment f
                            word_num=word_num+1


                        # This is the case when the full word cannot be accomodated in the same line and so we just add blank
                        # spaces to the rest of the line
                        else:

                            # We generate k number of blank spaces since we cannot accomodate any word on that line
                            line_output=generate_blank(line_output,k,True,_base_path)

                            # Debug var
                            MY_OUTPUT = MY_OUTPUT.ljust(k + len(MY_OUTPUT), ' ')

                            # END OF LINE, k>0 condition will fail in the above while loop
                            k=-1

                # This is the case when we have encountered a '\n' word. We now need to add an empty line
                else:

                    # We check if '\n' is not the first word
                    if(k!=60):

                        # We generate as many blank spaces as are left on that line, ie k
                        line_output = generate_blank(line_output, k, True,_base_path)

                        #Debug Variable
                        MY_OUTPUT = MY_OUTPUT.ljust(k + len(MY_OUTPUT), ' ')

                        # END OF LINE
                        k = -1

                        # Increment the word('\n')
                        word_num=word_num+1

                    # This is the case when '\n' is the first word
                    else:

                        # We generate 60 blanks, which is = k.
                        # Note the only difference here is that k__k is false since we don't have a previous image
                        line_output = generate_blank(line_output, k, False,_base_path)

                        #Debug var
                        MY_OUTPUT = MY_OUTPUT.ljust(k + len(MY_OUTPUT), ' ')

                        # End of line
                        k=-1

                        # Increment the word('\n')
                        word_num=word_num+1

            # In the case that some random error occurs, we just add that many blank spaces to the line:)
            except IndexError:
                line_output = generate_blank(line_output, k, True,_base_path)

                #Debug Variable
                MY_OUTPUT = MY_OUTPUT.ljust(k + len(MY_OUTPUT), ' ')

                # END OF LINE
                k=-1
                pass

        # Debug var
        MY_OUTPUT = MY_OUTPUT + '!'
        MY_SENTENCE_OUTPUT.append(MY_OUTPUT)
        MY_OUTPUT = ''

        # Sentences hols all the sentences. line_output is the output for that line
        sentences.append(line_output)
        line_output = 0

    # Debug printing
    for i in range(len(MY_SENTENCE_OUTPUT)):
        print(MY_SENTENCE_OUTPUT[i])

    # Concatenatig all sentences to produce the final image
    final_output = sentences[0]
    print(final_output.shape)
    for i in range(1,len(sentences)):
        print(sentences[i].shape)
        final_output = np.concatenate((final_output, sentences[i]), axis=0)

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


    path = _base_path + 'result.jpg'
    cv2.imwrite(path, border)

    return border

def add(request):
    request.session["txt"] = request.GET["text_string"]
    return render( request, "choice.html" )

def upload(request):

    if request.method == "POST":

        # Get the file, input text and reference to filesystem object
        myfile      = request.FILES["myfile"]
        inp_text    = request.session["txt"]
        fs          = FileSystemStorage()

        # Get the current time and convert it to an ID
        cur_time    = to_id( time.time_ns() )

        # Relative paths to the scan folder, submission, processed submission and result
        dir_path    = "media\\AllHandwritings\\scan_{}".format( cur_time )
        sub_path    = dir_path + "\\submission.jpg"
        pro_path    = dir_path + "\\processed_submission.jpg"
        res_path    = dir_path + "\\result.jpg"

        # Create directory and save submission
        os.mkdir( dir_path )
        filename    = fs.save( "AllHandwritings\\scan_{}\\submission.jpg".format( cur_time ), myfile )

        # Preprocess submission and detect boxes
        preprocess( sub_path, pro_path )
        detect_box( pro_path, dir_path )

        # Generate handwritten image
        img         = handwrite( inp_text, dir_path + '\\' )
        upload_url  = fs.url( filename )
        new_url     = res_path

        return render( request, 'result.html', {'image':new_url} )
