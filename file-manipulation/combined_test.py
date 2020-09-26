from img import image_processing as ip
from pdf import pdf_processing as pp
import os

# get access to a file in a sub directory
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'pdf/matricula_p9.pdf')

# get all the jpgs from the pdf
lst = pp.get_jpgs(filename)

# for every image in the list
for image in lst:
    # load the image and double its scale
    display_img = ip.scale(ip.read(image), 200)

    # process the image
    display_img = ip.blur(
        ip.denoise(
            ip.invert_bw(
                ip.color_mask(display_img, 90, 8)),
            3),
        3)

    # display the image
    ip.display(display_img, 50)
