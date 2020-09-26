"""
Auth: Nate Koike
Desc: a module to process images
Date: 23 September 2020, started;
"""

import cv2 #  image processing
import numpy as np # extra math
import threading # multithreading

# read an image and return the image object
def read(fname):
    return cv2.imread(fname)

# rescale an image
def scale(image, percent=100):
    height = int(image.shape[0] * percent / 100)
    width = int(image.shape[1] * percent / 100)

    return cv2.resize(image, (width, height))

# display an image, closing the window when the escape key is pressed
def display(image, size=100):
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
            cv2.THRESH_BINARY, 7, 15)

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

# find and return the darkest color in the image
# TODO: add multithreading to increase speed
def get_darkest(image, step=4):
    # a placeholder for the darkext pixel value, this value is pure white and
    # should be overwritten later
    darkest = [255, 255, 255]

    # look at fourth row
    for i in range(0, len(image), step):
        row = image[i]
        # look at every fourth pixel
        for j in range(0, len(row), step):
            pixel = row[j]
            if sum(pixel) < sum(darkest):
                darkest = pixel


    return darkest

# apply a color mask to the image
def color_mask(image, max, step=4, magic=False):
    # check to see if we should use magic numbers
    if magic:
        # change the colorspace of the image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # set the lower color bound as black
        low = np.array([0, 0, 0])

        # take the user's magic number input for the max brightnesss
        high = np.array([max, max, max])

    # use smart color masking
    else:
        # the darkest value allowed by the color mask
        low = get_darkest(image, step)

        # the lightest value allowed by the color mask
        high = np.array([
            np.uint8(low[0] + max),
            np.uint8(low[1] + max),
            np.uint8(low[2] + max)])

    # apply the color mask and return the color masked image
    return cv2.inRange(image, low, high)

# invert the black and white sections
def invert_bw(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV)[1]

# project horizontal lines where the program thinks like breaks should be

# get the first line of text in the image
def get_first_line(image):
    pass
