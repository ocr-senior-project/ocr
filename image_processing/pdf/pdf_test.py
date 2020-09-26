"""
Auth: Nate Koike
Date: 25 September 2020
Desc: a quick script to rip all jpgs from a pdf
"""

# Extract jpg's from pdf's. Quick and dirty.
import time

fpath = "matricula_p9.pdf"
encoding = "ansi"
start_tag = "ÿØÿà"
end_tag = "endstream"

# open the pdf
file = open(fpath, "rb")

# read the pdf and decode it into a string
pdf = file.read().decode(encoding)

# close the file
file.close()

# the starting index to search from
start = 0

# the total number of images found
n_images = 0

while start >= 0:
    # try to find a new stream
    try:
        # find the word ">>stream" in the pdf. this denotes that some stream follows
        stream_start = pdf.find(start_tag, start)
        print("start:", stream_start)
    except:
        # if there is no new stream then just exit
        break

    stream_end = pdf.find(end_tag, stream_start)
    print("end:", stream_end)

    # select up to the end of the stream
    stream = pdf[stream_start: stream_end]

    print(stream[0:10])

    # check for an image
    if "ÿØÿà" in stream:
        # open a .jpg file for writing bytes
        jpg = open("jpg" + str(n_images) + ".jpg", "wb")

        # encode and write the bytes
        jpg.write(stream.encode(encoding))

        # close the file
        jpg.close()
        print("written")

        # increment the total number of images found
        n_images += 1

    start = stream_end

    # give time to kill the program
    time.sleep(1)
