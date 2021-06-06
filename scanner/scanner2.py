
import cv2, math, numpy as np
import time

def detect_box( image, line_min_width = 24 ):

    image = cv2.imread( image )

    # Convert ot grayscale and binarize
    gray_scale          = cv2.cvtColor( image, cv2.COLOR_BGR2GRAY )
    th1, img_bin        = cv2.threshold( gray_scale, 200, 255, cv2.THRESH_BINARY )

    cv2.imshow( 'bin', ~img_bin )

    # Run kernels to remove non-essential details
    kernal_h            = np.ones( (1, line_min_width), np.uint8 )
    kernal_v            = np.ones( (line_min_width, 1), np.uint8 )
    img_bin_h           = cv2.morphologyEx( ~img_bin, cv2.MORPH_OPEN, kernal_h )
    img_bin_v           = cv2.morphologyEx( ~img_bin, cv2.MORPH_OPEN, kernal_v )

    # Get the resultant or of the two kernelled images
    img_bin_final       = img_bin_h | img_bin_v
    final_kernel        = np.ones((4,4), np.uint8)
    img_bin_final       = cv2.dilate( img_bin_final, final_kernel, iterations = 1 )

    cv2.imshow( 'kernel', img_bin_final )

    ret, labels, stats,centroids = cv2.connectedComponentsWithStats(~img_bin_final, connectivity=8, ltype=cv2.CV_32S)

    for x,y,w,h,area in stats[2:]:
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)

    cv2.imshow( 'final', image )

detect_box('scanner\\scan_final_.jpg')
cv2.waitKey(0)
cv2.destroyAllWindows()