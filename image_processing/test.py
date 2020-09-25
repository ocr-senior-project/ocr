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

# # realign the image
# img = ip.deskew(img)
# ip.display(img)

# # apply thresholding
# img = ip.threshold(img)
# ip.display(img)
#
# # denoise the image
# img = ip.denoise(img)
# ip.display(img)

# mask the image
img = ip.color_mask(img)
ip.display(img)
