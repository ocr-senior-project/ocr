import os # needed for path
# import cv2
import image_processing as ip

# fpath = os.path.relpath("matricula_p9-page-001.jpg")
fpath = "matricula_p9-page-001.jpg"

# image scale
scale = 40

img = ip.read(fpath)

ip.display(img, scale)

# mask the image (magic mode)
img = ip.color_mask(img, 185, magic=True)
ip.display(img, scale)

img = ip.deskew(img)

# # mask the image
# img = ip.color_mask(img, 90)
ip.display(img, scale)

# invert the black and white sections
img = ip.invert_bw(img)
ip.display(img, scale)

# denoise the image
img = ip.denoise(img, 3)
ip.display(img, scale)

# slightly blur the image
img = ip.blur(img, 3)
ip.display(img, scale)

lines = ip.get_lines(img, change=10)

for line in lines:
    ip.project(img, line)

ip.display(img, scale)

ip.write("out.jpg", img)
