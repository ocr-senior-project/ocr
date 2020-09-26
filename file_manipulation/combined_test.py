from img import image_processing as ip
from pdf import pdf_processing as pp
import os

# get access to a file in a subdirectory
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'matricula.pdf')

# get all the jpgs from the pdf
lst = pp.get_jpgs(filename, wait=True)
# lst=[1]
print(len(lst))

# for every image in the list
for image in lst:
    # load the image and double its scale
    display_img = ip.scale(ip.read("jpg0.jpg"), 200)

    # process the image
    display_img = ip.blur(
        ip.denoise(
            ip.invert_bw(
                ip.color_mask(display_img, 90, 8)),
            3),
        3)

    # display the image
    ip.display(display_img, 100)
