import numpy as np
import cv2

# Load image and convert to grayscale (temporary for finding contours)
img = cv2.imread('scan.jpg')
imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Convert the image from grayscale to black and white by applying a threshold of 240
_, thrash = cv2.threshold(imgGrey, 240, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
# contours, _ = cv2.findContours(imgGrey, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

# cv2.imshow("img", img)

cntr = 0

for contour in contours:
    approx = cv2.approxPolyDP(contour, 0.01* cv2.arcLength(contour, True), True)
    x = approx.ravel()[0] - 5
    y = approx.ravel()[1] - 5

    if len(approx) == 4:
        x1 ,y1, w, h = cv2.boundingRect(approx)
        if w*h < 50 or w*h >= 1400*600: continue
        aspectRatio = float(w)/h
        print(aspectRatio)
        cv2.putText(img, "rectangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
        cv2.drawContours(img, [approx], 0, (0, 255, 0), 5)
        cntr += 1

        # if aspectRatio >= 0.95 and aspectRatio <= 1.05:
        # pass
        # else:
        # pass


cv2.imshow("shapes", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
print(cntr)