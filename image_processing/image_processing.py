"""
Auth: Nate Koike
Desc: a module to process images
Date: 23 September 2020
"""

import cv2
import numpy as np

# read an image and return the image object
def read(fname):
    return cv2.imread(fname)

# display an image, closing the window when the escape key is pressed
def display(image):
    # resize the output window to be 720p
    cv2.imshow("image", cv2.resize(image, (1280, 720)))

    # loop until the window is closed
    while True:
        # press the escape key to quit
        if cv2.waitKey(0):
            cv2.destroyAllWindows()
            break

# remove small pieces of noise
def threshold(image):
    return cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY, 9, 11)

# noise removal
def denoise(image):
    return cv2.medianBlur(image, 3)

# force an image into grayscale
def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# realign a grayscale image
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

# apply a gaussian blur to the image
def blur(image):
     return cv2.GaussianBlur(image, (5, 5), 0)

def color_mask(image):
    hsv_color = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    low = np.array([0, 0, 0])

    max = 190

    high = np.array([max, max, max])
    mask = cv2.inRange(hsv_color, low, high)

    mask = blur(mask)

    return mask

# get the first line of text in the image
def get_first_line(image):
    pass
