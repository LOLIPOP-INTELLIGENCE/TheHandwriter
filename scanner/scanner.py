
import cv2, math, numpy as np
import resizer as rsz

name_lst = [['a_small', 'b_small', 'c_small', 'd_small', 'e_small', 'f_small', 'g_small', 'h_small', 'i_small', 'j_small', 'k_small', 'l_small', 'm_small', 'n_small', 'o_small', 'p_small', 'q_small', 'r_small', 's_small', 't_small'],
            ['u_small', 'v_small', 'w_small', 'x_small', 'y_small', 'z_small', 'a_big', 'b_big', 'c_big', 'd_big', 'e_big', 'f_big', 'g_big', 'h_big', 'i_big', 'j_big', 'k_big', 'l_big', 'm_big', 'n_big'],
            ['o_big', 'p_big', 'q_big', 'r_big', 's_big', 't_big', 'u_big', 'v_big', 'w_big', 'x_big', 'y_big', 'z_big', 'dot', 'comma', 'question']]

crop_img = lambda  _x, _y, _w, _h, _img : _img[_y:_y+_h , _x:_x+_w]

def detect_box( image, line_min_width = 38 ):

    image = cv2.imread( image )

    # Minimum line widths for horizontal and vertical axis (in pixels)
    line_min_width_ver  = 60
    line_min_width_hor  = 38

    # Convert ot grayscale and binarize
    gray_scale          = cv2.cvtColor( image, cv2.COLOR_BGR2GRAY )
    th1, img_bin        = cv2.threshold( gray_scale, 200, 255, cv2.THRESH_BINARY )

    # Run kernels to remove non-essential details
    kernal_h            = np.ones( (1, line_min_width), np.uint8 )
    kernal_v            = np.ones( (line_min_width, 1), np.uint8 )
    img_bin_h           = cv2.morphologyEx( ~img_bin, cv2.MORPH_OPEN, kernal_h )
    img_bin_v           = cv2.morphologyEx( ~img_bin, cv2.MORPH_OPEN, kernal_v )

    # Get the resultant or of the two kernelled images
    img_bin_final       = img_bin_h | img_bin_v
    final_kernel        = np.ones((4, 4), np.uint8)
    img_bin_final       = cv2.dilate( img_bin_final, final_kernel, iterations = 1 )

    # Get connected components and remove residual components
    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(~img_bin_final, connectivity = 8, ltype = cv2.CV_32S)
    stats = stats[2:]

    max_rows            = 20
    row                 = 0
    lst                 = [[] for i in range( max_rows )]
    unfilt_lst          = []

    for x, y, w, h, area in stats:
        unfilt_lst.append([y, x, h, w])

    unfilt_lst.sort()

    for y, x, h, w in unfilt_lst:
        lst[ row // max_rows ].append([x, y, w, h])
        row += 1

    for i in range( max_rows ):
        lst[i].sort()

    for i in range( max_rows ):
        j = 0
        for x, y, w, h in lst[i]:
            cropped_img = crop_img( x, y, w, h, image )
            cv2.imwrite( 'scanner\\results\\{}.jpg'.format( name_lst[i][j] ), cropped_img )
            j += 1

    for y, x, h, w in unfilt_lst:
        cv2.rectangle( image, (x, y), (x+w, y+h), (0, 255, 0), 1 )

    cv2.imshow( 'final', image )

rsz.preprocess('scanner\\scans\\real_filled.jpeg')
detect_box('scanner\\scan_final_.jpg')

cv2.waitKey(0)
cv2.destroyAllWindows()
