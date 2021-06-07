import cv2, math, numpy as np
import pygame

name_lst = [['a_small', 'b_small', 'c_small', 'd_small', 'e_small', 'f_small', 'g_small', 'h_small', 'i_small', 'j_small', 'k_small', 'l_small', 'm_small', 'n_small', 'o_small', 'p_small', 'q_small', 'r_small', 's_small', 't_small'],
            ['u_small', 'v_small', 'w_small', 'x_small', 'y_small', 'z_small', 'a_big', 'b_big', 'c_big', 'd_big', 'e_big', 'f_big', 'g_big', 'h_big', 'i_big', 'j_big', 'k_big', 'l_big', 'm_big', 'n_big'],
            ['o_big', 'p_big', 'q_big', 'r_big', 's_big', 't_big', 'u_big', 'v_big', 'w_big', 'x_big', 'y_big', 'z_big', 'dot', 'comma', 'question']]

# Utility function to get cropped image
crop_img = lambda  _x, _y, _w, _h, _img : _img[_y:_y+_h , _x:_x+_w]

# Function to resize the image to constant width
def preprocess( _surf ):

    # Load the image and get dinensions
    _surf           = pygame.image.load( _surf )
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
    pygame.image.save( _surf, 'scanner\\scans\\scan_final.jpg' )

# Function to go through image and find rects
def detect_box( _image ):

    # Load the image
    image               = cv2.imread( _image )
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
    final_kernel        = np.ones((4, 4), np.uint8)
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
            cropped_img = crop_img( x, y, w, h, image )
            cv2.imwrite( 'scanner\\results\\{}.jpg'.format( name_lst[i][j] ), cropped_img )

preprocess('scanner\\scans\\real_filled.jpeg')
detect_box('scanner\\scans\\scan_final.jpg')
