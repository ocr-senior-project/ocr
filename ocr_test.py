from HandwritingRecognitionSystem_v2.config import cfg

from ocr import *

file = open("ocr_output.txt", "w")

# ocr(output, charset_path, img_list_path, img_dir, model_dir):
ocr(file,
    "./HandwritingRecognitionSystem_v2/formalsamples/CHAR_LIST",
    "./HandwritingRecognitionSystem_v2/formalsamples/list",
    "./HandwritingRecognitionSystem_v2/formalsamples/images",
    "./HandwritingRecognitionSystem_v2/MATRICULAmodel/")
