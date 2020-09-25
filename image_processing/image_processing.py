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

# rescale an image
def scale(image, percent=100):
    height = int(image.shape[0] * percent / 100)
    width = int(image.shape[1] * percent / 100)

    return cv2.resize(image, (width, height))

# display an image, closing the window when the escape key is pressed
def display(image, size):
    # resize the output window to be 720p
    cv2.imshow("image", scale(image, size))

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
def denoise(image, ksize):
    return cv2.medianBlur(image, ksize)

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
def blur(image, sigma):
     return cv2.GaussianBlur(image, (sigma, sigma), 0)

# apply a color mask to the image
def color_mask(image, max):
    hsv_color = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # the darkest value allowed by the color mask
    low = np.array([0, 0, 0])

    # the lightest value allowed by the color mask
    high = np.array([max, max, max])

    # apply the color mask to the image
    mask = cv2.inRange(hsv_color, low, high)

    return mask

# invert the black and white sections
def invert_bw(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV)[1]

# get the first line of text in the image
def get_first_line(image):
    pass
