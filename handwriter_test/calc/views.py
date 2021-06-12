from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

import time, os
import numpy as np
import cv2, pygame
import math, random
from PIL import Image

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
            ['o_b', 'p_b', 'q_b', 'r_b', 's_b', 't_b', 'u_b', 'v_b', 'w_b', 'x_b', 'y_b', 'z_b', 'dot_x', 'comma_x', 'question_x', 'blank1_x']]

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

def hand_w(input_string, _base_path):
    contents=input_string
    contents=contents.strip()
    words=contents.split(" ")


    print(words)
    print(len(words))
    tau=len(words)
    i=0
    while(i<tau):
        if(words[i].startswith('\n') or words[i].startswith('\\n')):
            if(words[i].startswith('\n')):
                word_t=(words[i][1:])
            else:
                word_t=(words[i][2:])
            words.insert(i,'\n')
            words[i+1]=word_t
            tau=tau+1
        i=i+1

    try:
        while True:
            words.remove('')
    except ValueError:
        pass

    #generate random errors
    l=0
    pop=0
    errors_for_number_for_words=13

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

    print(words)
    print(len(words))

    return func_two(words, _base_path)

def generate_word(img_prev, word__k, k,N___K,K___K,add_blank, base_path):

    base_path = base_path

    #Random Set of Letters
    value = random.randint(2,3)
    #Random Error
    value_err = random.randint(1,11)

    #Retrieving path of revelant character
    sentence__k     = list(word__k)
    str_sent__k0    = str( sentence__k[0] )
    str_val         = str( value )

    special_dct     = {'?':'question', ' ':'blank2', '\n':'blank2', '~':'error'}

    fil_name        = '{}.jpg'

    if str_sent__k0.islower():      fil_name = fil_name.format( str_sent__k0 + '_s' )
    elif str_sent__k0.isupper():    fil_name = fil_name.format( str_sent__k0 + '_b' )
    elif str_sent__k0.isdigit():    fil_name = fil_name.format( str_sent__k0 + '_d' )
    else:                           fil_name = fil_name.format( special_dct.get( str_sent__k0, 'blank1' ) + '_x' )

    path__k = base_path + fil_name

    # print('not in loop', path__k)

    #creating the first image
    degree=random.randint(-10,0)
    img = cv2.imread(path__k)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    black_low = np.array([0, 0, 0])
    black_high = np.array([50, 50, 50])
    mask = cv2.inRange(hsv, black_low, black_high)
    color_shade=random.randint(0,50)
    img[mask > 0] = (color_shade,color_shade,color_shade)
    border = cv2.copyMakeBorder(
        img,
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
    img = cv2.resize(im_np, (40, 114))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_np = np.array(img)
    final_img = img_np
    #doing the above for n-1 characters
    for i in range(1, len(sentence__k)):
        value_err = random.randint(1, 11)
        value = random.randint(2, 3)

        #DEGREE OF ROTATION FOR PHYSICS PROJECT
        #degree=random.randint(-6,6)

        #REAL DEGREE OF ROTATION
        degree          = random.randint(-10,10)
        str_sent__ki    = str( sentence__k[i] )
        str_val         = str( value )

        fil_name        = '{}.jpg'

        if str_sent__ki.islower():      fil_name = fil_name.format( str_sent__ki + '_s' )
        elif str_sent__ki.isupper():    fil_name = fil_name.format( str_sent__ki + '_b' )
        elif str_sent__ki.isdigit():    fil_name = fil_name.format( str_sent__ki + '_d' )
        else:                           fil_name = fil_name.format( special_dct.get( str_sent__ki, 'blank1' ) + '_x' )

        path            = base_path + fil_name

        # print('in i loop', path)
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


    #This is there to add the image of previous words from img_prev
    if (k):
        final_img = np.concatenate((img_prev, final_img), axis=1)
    if(add_blank):
        final_img = generate_blank(img_prev__k=final_img, N__k=N___K, k__k=K___K,base_path=base_path)

    return final_img



#Very similar logic for generating blank space
def generate_blank(img_prev__k, N__k, k__k, base_path):

    if(N__k>0):
        path = base_path + 'blank1_x.jpg'
        print(path)
        img = cv2.imread(path, 0)
        img = cv2.resize(img, (40, 114))
        img_np = np.array(img)
        final_img = img_np
        for i in range(1, N__k):
            path = base_path + 'blank1_x.jpg'
            img2 = cv2.imread(path, 0)
            img2 = cv2.resize(img2, (40, 114))
            img_np2 = np.array(img2)
            final_img = np.concatenate((img_np, img_np2), axis=1)
            img_np = final_img
        if (k__k):
            final_img = np.concatenate((img_prev__k, final_img), axis=1)

        return final_img
    else:
        return img_prev__k

#f-word number
def func_two(words,_base_path):
    f=0
    #line output
    output=0
    #array of sentences
    sentences=[]

    MY_OUTPUT=''
    MY_SENTENCE_OUTPUT=[]
    while(f<len(words)):
        k=60
        #Adding 60 characters in a line
        while(k>0):
            try:
                if(words[f]!='\n'):
                    if(k==60):
                        X=random.randint(1,2)
                        output=generate_blank(img_prev__k=0,N__k=X,k__k=False,base_path=_base_path)
                        k=k-X
                        output = generate_word(img_prev=output, word__k=words[f], k=True, N___K=3, K___K=True, add_blank=True,base_path=_base_path)
                        MY_OUTPUT = MY_OUTPUT + words[f] + '   '
                        k=k-(len(words[f])+3)
                        f=f+1
                    else:
                        if(k-len(words[f])>=0):
                            t=min(3,k-len(words[f]))
                            output = generate_word(img_prev=output, word__k=words[f], k=True, N___K=t, K___K=True, add_blank=True,base_path=_base_path)
                            MY_OUTPUT=MY_OUTPUT+words[f]
                            MY_OUTPUT = MY_OUTPUT.ljust(t + len(MY_OUTPUT), ' ')
                            k=k-(len(words[f])+t)
                            f=f+1

                        else:
                            output=generate_blank(img_prev__k=output,N__k=k,k__k=True,base_path=_base_path)
                            MY_OUTPUT = MY_OUTPUT.ljust(k + len(MY_OUTPUT), ' ')
                            k=-1
                else:
                    if(k!=60):
                        output = generate_blank(img_prev__k=output, N__k=k, k__k=True,base_path=_base_path)
                        MY_OUTPUT = MY_OUTPUT.ljust(k + len(MY_OUTPUT), ' ')
                        k = -1
                        f=f+1
                    else:
                        output = generate_blank(img_prev__k=output, N__k=k, k__k=False,base_path=_base_path)
                        MY_OUTPUT = MY_OUTPUT.ljust(k + len(MY_OUTPUT), ' ')
                        k=-1
                        f=f+1
            except IndexError:
                output = generate_blank(img_prev__k=output, N__k=k, k__k=True,base_path=_base_path)
                MY_OUTPUT = MY_OUTPUT.ljust(k + len(MY_OUTPUT), ' ')
                k=-1
                pass

        MY_OUTPUT = MY_OUTPUT + '!'
        MY_SENTENCE_OUTPUT.append(MY_OUTPUT)
        MY_OUTPUT = ''
        sentences.append(output)
        output = 0


    for i in range(len(MY_SENTENCE_OUTPUT)):
        print(MY_SENTENCE_OUTPUT[i])

    final_output = sentences[0]
    print(final_output.shape)
    for i in range(1,len(sentences)):
        print(sentences[i].shape)
        final_output = np.concatenate((final_output, sentences[i]), axis=0)

    #REAL BORDER VALUES
    border = cv2.copyMakeBorder(
        final_output,
        top=120,
        bottom=40,
        left=100,
        right=30,
        borderType=cv2.BORDER_CONSTANT,
        value=[255,255,255]
    )

    path = 'D:\TheHandwriter\handwriter_test\static\FINAL_RESULToutput.png'
    cv2.imwrite(path, border)

    return border

def home(request):
    return render(request, 'home.html', {'name': ''})

# user_input=''
def add(request):
    # global user_input
    # user_input = request.GET['text_string']

    # my_uid = base_converter( time.time_ns() )
    request.session['txt'] = request.GET['text_string']

    # print('\n\nAdd:', request.session['uid'], '\n\n')

    return render(request, "choice.html")

def upload(request):
    # user_input=''
    # if request.method == 'GET':
    #     user_input=request.GET['text_string']   
    #     print(user_input)

    if request.method == 'POST':
        #  and request.FILES['myfile']
        # print('\n\nUpl:', request.session['uid'], '\n\n')
        # txt_name=request.POST['text_string']
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()

        cur_time = time.time_ns()
        dir_path = "scan_{}".format( cur_time )

        os.mkdir("media_cdn\\AllHandwritings\\{}".format( dir_path ))
        # print('\t\t', os.getcwd())
        os.system("python ./manage.py collectstatic --noinput")

        filename = fs.save("AllHandwritings\\{}\\submission.jpg".format( dir_path ), myfile)

        preprocess("media_cdn\\AllHandwritings\\{}\\submission.jpg".format( dir_path ), "media_cdn\\AllHandwritings\\{}\\processed_submission.jpg".format( dir_path ))
        detect_box("media_cdn\\AllHandwritings\\{}\\processed_submission.jpg".format( dir_path ), "media_cdn\\AllHandwritings\\{}".format( dir_path ))

        img = hand_w(request.session['txt'], "media_cdn\\AllHandwritings\\{}\\".format( dir_path ) )
        # cv2.imwrite( "media_cdn\\AllHandwritings\\{}\\result.jpg".format( dir_path ), img )

        uploaded_file_url = fs.url(filename)
        return render(request, 'result.html')
    # return render(request, 'io.html')

def own_handwriting(request):
    return render(request, "io.html")

def base_converter( _num, _base = 64 ):

    if _num:
        charset = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_#'
        res     = ''

        while _num:
            rem     = _num % _base
            _num    //= _base
            res     += charset[rem]

        return res[::-1]
    return '0'