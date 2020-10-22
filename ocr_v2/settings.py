"""
Auth: Nate Koike, Roger Danilek
Date: 16 October 2020
Desc: handle settings and utility for the ocr library
"""

import cnn
import rnn

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
    def __init__(self, char_list, save, model, log, start):
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
        self.fv = int(WND_HEIGHT / (2 ** maxpool))

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

    # process a single string
    def run(self, img):
        vec_per_win = self.width / math.pow(2, MPoolLayers_H)

        # blank image placeholder
        x = tf.zeros([None, WND_HEIGHT, WND_WIDTH])

        # Create a blank array for 1 output?
        seq_lens = tf.zeros([1])

        # insert a fourth dimension at the end of the tensor
        x_expanded = tf.expand_dims(x, 3)

        # create the inputs for the rnn
        ins = CNN(x_expanded, phase_train, 'CNN')

        # get the raw prediction for one character
        logits = RNN(ins, seq_lens, 'RNN')

        # decode prediction string from the probability map (logits)
        decoded, log_prob = tf.nn.ctc_beam_search_decoder(inputs=logits, sequence_length=SeqLens)

        #Reading test data...
        InputListTest, SeqLensTest, _ = ReadData(cfg.TEST_LOCATION, cfg.TEST_LIST, cfg.TEST_NB, WND_HEIGHT, WND_WIDTH, WND_SHIFT, VEC_PER_WND, '')

        print('Initializing...')

        session = tf.compat.v1.Session()

        session.run(tf.compat.v1.global_variables_initializer())

        LoadModel(session, cfg.SaveDir+'/')

        try:
        	session.run(tf.compat.v1.assign(phase_train, False))

        	randIxs = range(0, len(InputListTest))

        	start, end = (0, cfg.BatchSize)

        	batch = 0
        	while end <= len(InputListTest):
        		batchInputs = []
        		batchSeqLengths = []
        		for batchI, origI in enumerate(randIxs[start:end]):
        			batchInputs.extend(InputListTest[origI])
        			batchSeqLengths.append(SeqLensTest[origI])

        		feed = {x: batchInputs, SeqLens: batchSeqLengths}
        		del batchInputs, batchSeqLengths

        		Decoded = session.run([decoded], feed_dict=feed)[0]
        		del feed

        		trans = session.run(tf.sparse.to_dense(Decoded[0]))

        		for i in range(0, cfg.BatchSize):

        			fileIndex = cfg.BatchSize * batch + i
        			filename = FilesList[fileIndex].strip()
        			decodedStr = " "

        			for j in range(0, len(trans[i])):
        				if trans[i][j] == 0:
        					if (j != (len(trans[i]) - 1)):
        						if trans[i][j+1] == 0: break
        						else: decodedStr = "%s%s" % (decodedStr, Classes[trans[i][j]])
        					else:
        						break
        				else:
        					if trans[i][j] == (NClasses - 2):
        						if (j != 0): decodedStr = "%s " % (decodedStr)
        						else: continue
        					else:
        						decodedStr = "%s%s" % (decodedStr, Classes[trans[i][j]])

        			decodedStr = decodedStr.replace("<SPACE>", " ")

        			decodedStr = filename + decodedStr[:] + "\n"
        			if cfg.WriteDecodedToFile == True: DecodeLog.write(decodedStr)
        			else: print(decodedStr, end=' ')

        		start += cfg.BatchSize
        		end += cfg.BatchSize
        		batch += 1

        	DecodeLog.close()

        except (KeyboardInterrupt, SystemExit, Exception) as e:
        	print("[Error/Interruption] %s" % str(e))
        	print("Clossing TF Session...")
        	session.close()
        	print("Terminating Program...")
        	sys.exit(0)

    def read_run(VEC_PER_WND):

    	seqLens = []
    	inputList = []

    	with open(filesList) as listHandler:

    		imgNbr = 0
    		imageFiles = listHandler.readlines()[0:numberOfFiles]

    		for imageFile in imageFiles:

    			if filesLocation != '': tfile = imageFile.strip('\n')
    			else: tfile = os.path.basename(imageFile.strip('\n'))

    			################################################################
    			# Gathering the length of each sequence

    			if filesLocation != '': imageFilePath = filesLocation + "/" + tfile + cfg.ImageFileType
    			else: imageFilePath = imageFile.strip('\n') + cfg.ImageFileType

    			print ("Reading " + imageFilePath)

    			image = cv2.imread(imageFilePath, cv2.IMREAD_GRAYSCALE)

    			h, w = np.shape(image)

    			if(h > WND_HEIGHT): factor = WND_HEIGHT/float(h)
    			else: factor = 1.0

    			image = cv2.resize(image, None, fx=factor, fy=factor, interpolation = cv2.INTER_CUBIC)

    			h, w = np.shape(image)

    			winId = 0
    			wpd = 0
    			while True:

    				s = (winId * WND_SHIFT)
    				e = s + WND_WIDTH

    				if e > w:
    					sl = (winId+1) * VEC_PER_WND

    					if transDir != '':
    					    #Fix for small sequences
    					    if(len(targetList[imgNbr]) > sl):
    						    diff = len(targetList[imgNbr]) - sl
    						    wpd = int(math.ceil(float(diff) / VEC_PER_WND))
    						    sl = sl + wpd * VEC_PER_WND

    					seqLens.append(sl)

    					break

    				winId = winId + 1

    			################################################################
    			# Adding features

    			featuresSet = []

    			winId = 0
    			while True:

    				s = (winId * WND_SHIFT)
    				e = s + WND_WIDTH

    				if e > w:
    					pad = np.ones((h, (e - w)), np.uint8)*255
    					wnd = image[:h,s:w]
    					wnd = np.append(wnd, pad, axis=1)

    					if h < WND_HEIGHT:
    						pad = np.ones(((WND_HEIGHT - h), WND_WIDTH), np.uint8)*255
    						wnd = np.append(pad, wnd, axis=0)

    					featuresSet.append(wnd)

    					#Fix for small sequences
    					pad = np.ones((WND_HEIGHT, WND_WIDTH), np.uint8)*255

    					for i in range(wpd): featuresSet.append(pad)

    					break

    				wnd = image[:h,s:e]

    				if h < WND_HEIGHT:
    					pad = np.ones(((WND_HEIGHT - h), WND_WIDTH), np.uint8)*255
    					wnd = np.append(pad, wnd, axis=0)

    				featuresSet.append(wnd)
    				winId = winId + 1

    			################################################################
    			inputList.append(featuresSet)

    			imgNbr = imgNbr + 1
    			################################################################

    	if transDir != '':
    	    assert len(inputList) == len(targetList)

    	return inputList, seqLens
