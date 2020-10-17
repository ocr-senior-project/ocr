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
        self.LeakyReLU = True

        # ----------------------------------------------------------------------
        # -------------------------- RNN Parameters ----------------------------
        # ----------------------------------------------------------------------
        # Number of LSTM units per forward/backward layer
        self.NUnits = 256

        # Number of BLSTM layers
        self.NLayers = 3

        # ----------------------------------------------------------------------
        # ----------------------- training parameters --------------------------
        # ----------------------------------------------------------------------
        # The epoch number to start training from
        # = 0 to train from scratch, != 0 to resume from the latest checkpoint
        self.StartingEpoch = start

        # Learning rate
        self.LearningRate = 0.0005

        # Batch size
        self.BatchSize = 2 #This is actually the number of images to process each iteration

        # Randomize the order of batches each epoch
        self.RandomBatches = True

        # Maximum gradient norm
        self.MaxGradientNorm = 5

        # Save model each n epochs
        self.SaveEachNEpochs = 2

        # Run the training for n epochs
        self.NEpochs = 1024

        # Stop the training after n epochs with no improvement on validation
        self.TrainThreshold = 8
