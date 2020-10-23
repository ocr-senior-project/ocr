"""
Auth: Nate Koike, Roger Danilek
Date: 16 October 2020
Desc: handle settings and utility for the ocr library
"""

# open a file and split it by newlines
# returns a list of the lines in the file and total number of lines
def load_list(fpath, enc="utf-8"):
    '''
    load the charset into a string, using whitespace as a delineator
    return a list of characters and the length of the list
    fpath: the path to the file containing the character set used by the ocr
      enc: the encoding of the file. this is utf-8 by default
    '''
    # open the file as bytes
    file = open(fpath, "rb")

    # get the list by reading in the entire file, decoding it using the
    # specified encoding, then splitting it on whitespace (default parameter)
    lst = file.read().decode(enc).split()

    # close the file to avoid file handlers floating around
    file.close()

    return [lst, len(lst)]

class CFG():
    def __init__(self, char_list, save, model, log, start, maxpool, h_maxpool, last):
        # ----------------------------------------------------------------------
        # --------------------- Images and Label File Types --------------------
        # ----------------------------------------------------------------------
        # The file type of images
        self.img_type = '.png'

        # The extension of the file holding the ground-truth labels
        self.label_type = '.tru'

        # ----------------------------------------------------------------------
        # ----------------------- Character information ------------------------
        # ----------------------------------------------------------------------
        # Sorted list of classes/characters. First one must be <SPACE>
        self.char_list, self.n_chars = load_list(char_list)

        # ----------------------------------------------------------------------
        # ------------------ Model and Log Files and Directories ---------------
        # ----------------------------------------------------------------------
        # Directory where model checkpoints are saved
        self.save_dir = save

        # Name of the model checkpoints
        self.model_name = model

        # Log file
        self.log_file = log

        # ----------------------------------------------------------------------
        # ---------------------- Neural Net Parameters -------------------------
        # ----------------------------------------------------------------------
        # Extraction window height
        self.height = 64

        # Extraction window width
        self.width = 64

        # Window shift
        self.shift = self.width - 2

        # Number of all max pool layers
        self.all_maxpool_layers = maxpool

        # Number of max pool in horizontal dimension
        self.h_maxpool_layers = h_maxpool

        # Number of feature maps at the last conv layer
        self.last_layer = last

        # tbh idk what this is
        self.fv = int(self.height / (2 ** maxpool))

        # the number of features? idk
        self.n_features = self.fv * self.last_layer

        # ----------------------------------------------------------------------
        # -------------------------- CNN Parameters ----------------------------
        # ----------------------------------------------------------------------
        # Use Leaky ReLU or ReLU
        self.leaky = True

        # ----------------------------------------------------------------------
        # -------------------------- RNN Parameters ----------------------------
        # ----------------------------------------------------------------------
        # Number of LSTM units per forward/backward layer
        self.n_units = 256

        # Number of BLSTM layers
        self.n_layers = 3

        # ----------------------------------------------------------------------
        # ----------------------- training parameters --------------------------
        # ----------------------------------------------------------------------
        # add these later



    # def read_run(self, VEC_PER_WND):
    # 	seqLens = []
    # 	inputList = []
    #
    # 	with open(filesList) as listHandler:
    # 		imageFiles = listHandler.readlines()[0:numberOfFiles]
    #
    # 		for imageFile in imageFiles:
    #             # # Replace above line with
    #             # image_file = our image
    #
    # 			if filesLocation != '': tfile = imageFile.strip('\n')
    # 			else: tfile = os.path.basename(imageFile.strip('\n'))
    #
    # 			################################################################
    # 			# Gathering the length of each sequence
    #
    # 			if filesLocation != '': imageFilePath = filesLocation + "/" + tfile + cfg.ImageFileType
    # 			else: imageFilePath = imageFile.strip('\n') + cfg.ImageFileType
    #
    # 			print ("Reading " + imageFilePath)
    #
    # 			image = cv2.imread(imageFilePath, cv2.IMREAD_GRAYSCALE)
    #
    # 			h, w = np.shape(image)
    #
    # 			if(h > WND_HEIGHT): factor = WND_HEIGHT/float(h)
    # 			else: factor = 1.0
    #
    # 			image = cv2.resize(image, None, fx=factor, fy=factor, interpolation = cv2.INTER_CUBIC)
    #
    # 			h, w = np.shape(image)
    #
    # 			winId = 0
    # 			wpd = 0
    # 			while True:
    #
    # 				s = (winId * WND_SHIFT)
    # 				e = s + WND_WIDTH
    #
    # 				if e > w:
    # 					sl = (winId+1) * VEC_PER_WND
    #
    # 					if transDir != '':
    # 					    #Fix for small sequences
    # 					    if(len(targetList[0]) > sl):
    # 						    diff = len(targetList[0]) - sl
    # 						    wpd = math.ceil(diff / VEC_PER_WND)
    # 						    sl += wpd * VEC_PER_WND
    #
    # 					seqLens.append(sl)
    #
    # 					break
    #
    # 				winId = winId + 1
    #
    # 			################################################################
    # 			# Adding features
    #
    # 			featuresSet = []
    #
    # 			winId = 0
    # 			while True:
    #
    # 				s = (winId * WND_SHIFT)
    # 				e = s + WND_WIDTH
    #
    # 				if e > w:
    # 					pad = np.ones((h, (e - w)), np.uint8)*255
    # 					wnd = image[:h,s:w]
    # 					wnd = np.append(wnd, pad, axis=1)
    #
    # 					if h < WND_HEIGHT:
    # 						pad = np.ones(((WND_HEIGHT - h), WND_WIDTH), np.uint8)*255
    # 						wnd = np.append(pad, wnd, axis=0)
    #
    # 					featuresSet.append(wnd)
    #
    # 					#Fix for small sequences
    # 					pad = np.ones((WND_HEIGHT, WND_WIDTH), np.uint8)*255
    #
    # 					for i in range(wpd): featuresSet.append(pad)
    #
    # 					break
    #
    # 				wnd = image[:h,s:e]
    #
    # 				if h < WND_HEIGHT:
    # 					pad = np.ones(((WND_HEIGHT - h), WND_WIDTH), np.uint8)*255
    # 					wnd = np.append(pad, wnd, axis=0)
    #
    # 				featuresSet.append(wnd)
    # 				winId = winId + 1
    #
    # 			inputList.append(featuresSet)
    #
    # 	return inputList, seqLens
