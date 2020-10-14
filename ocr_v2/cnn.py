import tensorflow as tf
from settings import CFG

cfg = CFG()

class CNN:
    def __init__(self, height, width, maxpool, h_maxpool, last):
        # Extraction window height
        self._wnd_height = height

        # Extraction window width
        self._wnd_width = width

        # Window shift
        self._wnd_shift = width - 2

        # Number of all maxpool layers
        self._all_maxpool_layers = maxpool

        # Number of maxpool in horizontal dimension
        self._h_maxpool_layers = h_maxpool

        # Number of feature maps at the last conv layer
        self._last_filters = last

        # tbh idk what this is
        self._fv = int(WND_HEIGHT / (2 ** maxpool))

        # the number of features? idk
        self._n_features = self._fv * self._last_filters

    # generate a convolutional layer?
    def conv_layer(self, inp, filter_in, filter_out, training, scope):
    	with tf.compat.v1.variable_scope(scope):
            # generate a weight variable
    		weight = weight_variable([3, 3, filter_in, filter_out])

            # theres some condition, but idk what this means
    		if cfg.LeakyReLU:
    			return tf.nn.leaky_relu(
                    cfg.batch_norm_conv(
                        conv2d(inp, weight),
                        filter_out,
                        training))

			return tf.nn.relu(
                batch_norm_conv(
                    conv2d(inp, weight),
                    filter_out,
                    training))

    # run light training?
    def CNNLight(X, Training, Scope):
    	with tf.compat.v1.variable_scope(Scope):

    		ConvLayer1 = ConvLayer(X, 1, 64, Training, 'ConvLayer1')

    		MPool1 = max_pool(ConvLayer1, ksize=(2, 2), stride=(2, 2))

    		ConvLayer2 = ConvLayer(MPool1, 64, 128, Training, 'ConvLayer2')

    		MPool2 = max_pool(ConvLayer2, ksize=(2, 2), stride=(2, 2))

    		ConvLayer3 = ConvLayer(MPool2, 128, 256, Training, 'ConvLayer3')

    		ConvLayer4 = ConvLayer(ConvLayer3, 256, 256, Training, 'ConvLayer4')

    		MPool4 = max_pool(ConvLayer4, ksize=(2, 1), stride=(2, 1))

    		ConvLayer5 = ConvLayer(MPool4, 256, 512, Training, 'ConvLayer5')

    		ConvLayer6 = ConvLayer(ConvLayer5, 512, 512, Training, 'ConvLayer6')

    		MPool6 = max_pool(ConvLayer6, ksize=(2, 1), stride=(2, 1))

    		ConvLayer7 = ConvLayer(MPool6, 512, 512, Training, 'ConvLayer7')

    		MPool7 = max_pool(ConvLayer7, ksize=(2, 1), stride=(2, 1))

    		MPool7_T = tf.transpose(a=MPool7, perm=[0,2,1,3])

    		MPool7_T_RSH = tf.reshape(MPool7_T, [-1, FV, LastFilters])

    		return tf.reshape(MPool7_T_RSH, [-1, NFeatures])
