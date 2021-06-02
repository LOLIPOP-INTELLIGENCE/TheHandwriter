# Resize image (pad if ratio not valid)

# Go through image and find contours
# Reject contours with areas too big or too small

# Sort contours based on y coordinate into rows
# Sort rows based on x coordinate into cols

# Warp cropped image to match dimensions, label and store

import cv2, numpy as np

def check_area( contour ):
    area = cv2.contourArea( contour )
    if area < 20000: return 0
    elif area < 30000: return 1
    else: return 2

# Load image and convert to grayscale (temporary for finding contours)
img = cv2.imread('scanner\scan.jpg')
imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Convert the image from grayscale to black and white by applying a threshold of 240
_, thrash = cv2.threshold(imgGrey, 240, 255, cv2.THRESH_BINARY)
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

final_list[0].sort(key = lambda e : e[-1])
final_list[1].sort(key = lambda e : e[-1])
final_list[2].sort(key = lambda e : e[-1])

for index, rect, heir, area in final_list[1]:
    x, y, w, h = rect
    cv2.rectangle(img, (x, y), (x+w, y+h), (0,255,0), 1)
    print(area, heir)

cv2.imshow("shapes", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

print(len(final_list[0]))
print(len(final_list[1]))
print(len(final_list[2]))