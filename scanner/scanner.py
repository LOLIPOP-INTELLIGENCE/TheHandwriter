# Resize image (pad if ratio not valid)

# Go through image and find contours
# Reject contours with areas too big or too small

# Sort contours based on y coordinate into rows
# Sort rows based on x coordinate into cols

# Warp cropped image to match dimensions, label and store

import cv2, numpy as np
import math

def check_area( contour ):
    area = cv2.contourArea( contour )
    if area < 1200: return 0
    elif area < 2400: return 1
    else: return 2

# Load image and convert to grayscale (temporary for finding contours)
<<<<<<< HEAD
img = cv2.imread('scanner/handwriting_input.png')
=======
img = cv2.imread('scanner\scan2_.jpg')

>>>>>>> 7a0eaf658e98d455d26d673dac9342132b1a29f5
imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Convert the image from grayscale to black and white by applying a threshold of 240
thrash = cv2.Canny(imgGrey, 127, 255)
cv2.imshow('canny', thrash)

contours, hierarchy = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
hierarchy = hierarchy[0]

list_0 = [] # List of small contours
list_1 = [] # list of correct contours
list_2 = [] # List of big contours

final_list = [list_0, list_1, list_2]

for i in range(len(contours)):
    contour = contours[i]
    heir    = hierarchy[i]

    approx = cv2.approxPolyDP(contour, 0.01* cv2.arcLength(contour, True), True)

    if len(approx) == 4:
        rect = cv2.boundingRect(contour)
        box = cv2.minAreaRect(approx)
        box = cv2.boxPoints(box)
        box = np.int0(box)

        final_list[check_area(contour)].append([i, rect, list(heir), cv2.contourArea(contour)])

too_small = [elem[0] for elem in final_list[0]] + [elem[0] for elem in final_list[2]]
too_small = set(too_small)

cntr = 0

for index, rect, heir, area in final_list[1]:
    x, y, w, h = rect
    nxt, prv, child, parent = heir

    # The contours must not have any children of their own (apart from noise)
    # if child == -1 or child not in too_small: continue
    cv2.rectangle(img, (x, y), (x+w, y+h), (0,255,0), 1)
    cntr += 1

print(cntr, '\n')
print(len(final_list[0]))
print(len(final_list[1]))
print(len(final_list[2]))

cv2.imshow("shapes", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
