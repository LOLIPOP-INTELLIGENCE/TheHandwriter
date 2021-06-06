# Resize image (pad if ratio not valid)

# Go through image and find contours
# Reject contours with areas too big or too small

# Sort contours based on y coordinate into rows
# Sort rows based on x coordinate into cols

# Warp cropped image to match dimensions, label and store

import cv2, math, numpy as np
# import scanner.resizer as rsz

def get_img_part( _x1, _y1, _x2, _y2, _img ):
    return _img[ _x1:_x2 , _y1:_y2 ]

def check_area( _contour ):

    return 1

    area            = cv2.contourArea( _contour )
    optimal_area    = 2300
    percent_diff    = 33

    min_thresh      = int( ( optimal_area * ( 100 - percent_diff ) ) / 100 )
    max_thresh      = int( ( optimal_area * ( 100 + percent_diff ) ) / 100 )

    if area < min_thresh: return 0  # too small
    if area < max_thresh: return 1  # perfect size

    return 2                        # too big

# Load image and convert to grayscale (temporary for finding contours)
img         = cv2.imread( 'scanner\scan_final_ .jpg' )
img_grey    = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY )

# Convert the image from grayscale to black and white by applying a threshold of 240
canny_img   = cv2.Canny( img_grey, 32, 255 )
# canny_img   = img_grey
cv2.imshow('canny', canny_img)

_           = cv2.findContours( canny_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE )
contours    = _[0]
hierarchy   = _[1][0]

final_list  = [[], [], []]

for i in range( len( contours ) ):

    contour     = contours[i]
    heir        = hierarchy[i]

    approx      = cv2.approxPolyDP( contour, 0.01 * cv2.arcLength( contour, True ), True )

    if len( approx ) == 4:
        rect        = cv2.boundingRect( contour )
        box         = cv2.minAreaRect( approx )
        box         = cv2.boxPoints( box )
        box         = np.int0( box )

        final_list[check_area( contour )].append( [i, rect, list( heir ), cv2.contourArea( contour )])

too_small   = [elem[0] for elem in final_list[0]] + [elem[0] for elem in final_list[2]]
too_small   = set( too_small )

cntr        = 0

for index, rect, heir, area in final_list[1]:
    x, y, w, h = rect
    nxt, prv, child, parent = heir

    # The contours must not have any children of their own (apart from noise)
    if child == -1 or child not in too_small: continue
    cv2.rectangle( img, (x, y), (x+w, y+h), (0, 255, 0), 1 )
    cntr += 1

print(cntr, '\n')
print(len(final_list[0]))
print(len(final_list[1]))
print(len(final_list[2]))

cv2.imshow('shapes', img)
cv2.waitKey(0)
cv2.destroyAllWindows()