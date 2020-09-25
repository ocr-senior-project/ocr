import os # needed for path
# import cv2
import image_processing as ip

# fpath = os.path.relpath("matricula_p9-page-001.jpg")
fpath = "matricula_p9-page-001.jpg"

img = ip.read(fpath)

ip.display(img)

# # make the image grayscale
# img = ip.grayscale(img)
# ip.display(img)
#
# # realign the image
# img = ip.deskew(img)
# ip.display(img)
#
# # apply thresholding
# img = ip.threshold(img)
# ip.display(img)
#
# # denoise the image
# img = ip.denoise(img, 3)
# ip.display(img)

# mask the image
img = ip.color_mask(img)
ip.display(img)

# invert the black and white sections
img = ip.invert_bw(img)
ip.display(img)

# # slightly blur the image
# img = ip.blur(img, 3)
# ip.display(img)

# apply thresholding
# img = ip.threshold(img)
# ip.display(img)

# denoise the image
img = ip.denoise(img, 3)
ip.display(img)

# slightly blur the image
img = ip.blur(img, 5)
ip.display(img)
