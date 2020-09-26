"""
Auth: Nate Koike
Date: 25 September 2020
Desc: a slightly more refined way of ripping jpgs from a pdf
"""

# create jpg files for every jpg found in the pdf
# return a list of all the file names
def get_jpgs(fname, enc="Latin-1", start_tag="ÿØÿà", end_tag="endstream", wait=False):
    # open the file
    file = open(fname, "rb")

    # read the pdf and decode it into a string
    pdf = file.read().decode(enc)

    # close the file
    file.close()

    # the starting index to search from
    start = 0

    # the filenames of all the images found
    imgs = []

    # start gets set to -1 when it fails to find what its looking for
    while start >= 0:
        # find the starting end ending indicies of the bytes in the pdf where
        # there is a jpg image
        stream_start = pdf.find(start_tag, start)
        stream_end = pdf.find(end_tag, stream_start)

        # select all the bytes that makeup the jpg
        stream = pdf[stream_start: stream_end]

        # double check for an image (make sure the search didnt fail)
        if start_tag in stream:
            # save the filename so we can append it to the list as well
            img_name = "jpg" + str(len(imgs)) + ".jpg"

            # open a .jpg file for writing bytes and write the image to the file
            jpg = open(img_name, "wb")
            jpg.write(stream.encode(enc))

            # close the file
            jpg.close()

            # append the filename to the list
            imgs.append(img_name)

        # start looking at the end of the last jpg that was found
        start = stream_end

    # return the list of filenames
    return imgs
