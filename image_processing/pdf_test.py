# import PyPDF2
#
# from PIL import Image
#
# if __name__ == '__main__':
#     input1 = PyPDF2.PdfFileReader(open("matricula_p9.pdf", "rb"))
#     page0 = input1.getPage(0)
#     xObject = page0['/Resources']['/XObject'].getObject()
#
#     for obj in xObject:
#         if xObject[obj]['/Subtype'] == '/Image':
#             size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
#             data = xObject[obj].getData()
#             if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
#                 mode = "RGB"
#             else:
#                 mode = "P"
#
#             if xObject[obj]['/Filter'] == '/FlateDecode':
#                 img = Image.frombytes(mode, size, data)
#                 img.save(obj[1:] + ".png")
#             elif xObject[obj]['/Filter'] == '/DCTDecode':
#                 img = open(obj[1:] + ".jpg", "wb")
#                 img.write(data)
#                 img.close()
#             elif xObject[obj]['/Filter'] == '/JPXDecode':
#                 img = open(obj[1:] + ".jp2", "wb")
#                 img.write(data)
#                 img.close()

# Extract jpg's from pdf's. Quick and dirty.
import sys

# open the pdf
file = open(sys.argv[1], "rb")

# read the pdf into a string
pdf = str(file.read())

# close the file
file.close()


# loop starts here


# find the word ">>stream" in the pdf. this denotes that some stream follows
start = pdf.find(">>stream")
print(start)

end = pdf.find("endstream")
print(end)

# select up to the end of the stream
stream = pdf[start: end]


print(stream)
