import pdf_processing as pp

file = open("matricula_p9.pdf")

jpgs = pp.get_jpgs(file)

print(jpgs)
