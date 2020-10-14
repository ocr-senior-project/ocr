from ocr_v2 import ocr

out = open("out.txt", "w")
charset = "charset.lst"
img_lst = ""
img_dir = ""
model_dir = ""


ocr(out, charset, img_lst, img_dir, model_dir)
