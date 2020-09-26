"""
Auth: Nate Koike
Date: 25 September 2020
Desc: a slightly more refined way of ripping jpgs from a pdf
"""

# create jpg files for every jpg found in the pdf
# return a list of all the file names
def get_jpgs(
        file, # the pdf in question
        enc="ansi", # the file encoding (if known, otherwise default to ansi)
        start_tag="ÿØÿà", # the first characters of the jpg encoding (probably)
        end_tag="endstream" # the marker for the end of the embedded jpg file
    ):
    # read the pdf and decode it into a string
    pdf = file.read().decode(enc)

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
            fname = "jpg" + str(n_images) + ".jpg"

            # open a .jpg file for writing bytes and write the image to the file
            jpg = open(fname, "wb")
            jpg.write(stream.encode(enc))

            # close the file
            jpg.close()

            # append the filename to the list
            imgs.append(fname)

        # start looking at the end of the last jpg that was found
        start = stream_end

    # return the list of filenames
    return imgs
