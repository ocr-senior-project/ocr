class cfg():
    def __init__(self):
        # -------- Images and labels file type --------
        # The file type of images
        self.img_type = '.png'
        # The extension of the file holding the ground-truth labels
        self.label_type = '.tru'

        # -------- Training data configuration --------
        # Number of training images to process
        self.train_nb = 4

        # List of training data without file extension.
        self.train_list = './formalsamples/list'

        # Location of training data. Could be included in the data list.
        self.train_location = './formalsamples/Images/'

        # Location of training data transcriptions
        self.train_trans = './formalsamples/Labels/'

        # -------- Validation data configuration --------
        # Number of validation images to process
        self.val_nb = 4

        # List of validation data without file extension.
        self.val_list = './formalsamples/list'

        # Location of validation data. Could be included in the data list.
        self.val_location = './formalsamples/Images/'

        # Location of validation data transcriptions
        self.val_trans = './formalsamples/Labels/'

        # -------- Test data configuration --------
        # Number of test images to process
        self.test_nb = 6

        # List of test data without file extension.
        self.test_list = './formalsamples/list'

        # Location of test data. Could be included in the data list.
        self.test_location = './formalsamples/Images/'

        # Write the decoded text to file or stdout
        self.write_decoded = True

        # -------- Classes information --------
        # Sorted list of classes/characters. First one must be <SPACE>
        self.char_list = './samples/CHAR_LIST'

        # -------- Model and logs files and directories --------
        # Directory where model checkpoints are saved
        self.save_dir = './MATRICULAmodel'

        # Name of the model checkpoints
        self.model_name = 'MATRICULAmodel.ckpt'

        # Log file
        self.log_file = './log'

        # Directory to store Tensorflow summary information
        self.log_dir = './summary'

        # Directory to store posteriors for WFST decoder
        self.probs = './Probs'

        # -------- CNN parameters --------
        # Use Leaky ReLU or ReLU
        self.LeakyReLU = True

        # -------- RNN parameters --------
        # Number of LSTM units per forward/backward layer
        self.NUnits = 256

        # Number of BLSTM layers
        self.NLayers = 3

        # -------- training parameters --------
        # The epoch number to start training from
        self.StartingEpoch = 0 # = 0 to train from scratch, != 0 to resume from the latest checkpoint

        # Learning rate
        self.LearningRate = 0.0005

        # Batch size
        self.BatchSize = 2 #This is actually the number of images to process each iteration

        # Randomize the order of batches each epoch
        self.RandomBatches = True

        # Maximum gradient norm
        self.MaxGradientNorm = 5

        # Save model each n epochs
        self.SaveEachNEpochs = 1

        # Run the training for n epochs
        self.NEpochs = 1000

        # Stop the training after n epochs with no improvement on validation
        self.TrainThreshold = 20

    def load_list(fpath, enc="utf-8"):
        '''
        load the charset into a string, using whitespace as a delineator
        return a list of characters and the length of the list
        fpath: the path to the file containing the character set used by the ocr
          enc: the encoding of the file. this is utf-8 by default
        '''
        # open the file as bytes
        file = open(fpath, "rb")

        # get the charset by reading in the entire file, decoding it using the
        # specified encoding, then splitting it on whitespace (default parameter)
        charset = file.read().decode(enc).split()

        # close the file to avoid file handlers floating around
        file.close()

        return [charset, len(charset)]

    #Ref: https://stackoverflow.com/questions/33949786/how-could-i-use-batch-normalization-in-tensorflow
    def batch_norm_conv(x, n_out, phase_train):
        with tf.compat.v1.variable_scope('bn'):
            beta = tf.Variable(tf.constant(0.0, shape=[n_out]), name='beta', trainable=True)
            gamma = tf.Variable(tf.constant(1.0, shape=[n_out]), name='gamma', trainable=True)
            batch_mean, batch_var = tf.nn.moments(x=x, axes=[0,1,2], name='moments')
            ema = tf.train.ExponentialMovingAverage(decay=0.5)

            def mean_var_with_update():
                ema_apply_op = ema.apply([batch_mean, batch_var])
                with tf.control_dependencies([ema_apply_op]):
                    return tf.identity(batch_mean), tf.identity(batch_var)

            mean, var = tf.cond(pred=phase_train, true_fn=mean_var_with_update,
                                false_fn=lambda: (ema.average(batch_mean), ema.average(batch_var)))
            normed = tf.nn.batch_normalization(x, mean, var, beta, gamma, 1e-3)
        return normed
