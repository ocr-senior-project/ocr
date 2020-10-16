import tensorflow as tf
from settings import CFG

class CNN:
    def __init__(self, maxpool, h_maxpool, last, cfg):
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

        self._cfg = cfg

    def max_pool(self, x, ksize=(2, 2), stride=(2, 2)):
        # x is a Conv_Layer object, not whatever ConvLayer returned
        return tf.nn.max_pool2d(input=x.activate(), ksize=[1, ksize[0], ksize[1], 1], strides=[1, stride[0], stride[1], 1], padding='SAME')

    def build(self, x_in, training):
        # x is an inputted numpy array representing the image
        # create the hidden layers that make up the "black box" of our NN
        layer1 = Conv_Layer(x_in, 1, 64, training, self._cfg)
        layer2 = Conv_Layer(layer1, 64, 64, training, self._cfg)
        mpool2 = self.max_pool(layer2, ksize=(2,2), stride=(2,2))

        layer3 = Conv_Layer(mpool2, 64, 128, training, self._cfg)
        layer4 = Conv_Layer(layer3, 128, 128, training, self._cfg)
        mpool4 = self.max_pool(layer4, ksize=(2, 2), stride=(2, 2))

        layer5 = Conv_Layer(mpool4, 128, 256, training, self._cfg)
        layer6 = Conv_Layer(layer5, 256, 256, training, self._cfg)
        layer7 = Conv_Layer(layer6, 256, 256, training, self._cfg)
        mpool7 = self.max_pool(layer7, ksize=(2, 1), stride=(2, 1))

        layer8 = Conv_Layer(mpool7, 256, 512, training, self._cfg)
        layer9 = Conv_Layer(layer8, 512, 512, training, self._cfg)
        layer10 = Conv_Layer(layer9, 512, 512, training, self._cfg)
        mpool10 = self.max_pool(layer10, ksize=(2, 1), stride=(2, 1))

        layer11 = Conv_Layer(mpool10, 512, 512, training, self._cfg)
        layer12 = Conv_Layer(layer11, 512, 512, training, self._cfg)
        layer13 = Conv_Layer(layer12, 512, self._last_filters, training, self._cfg)
        mpool13 = self.max_pool(layer13, ksize=(2, 1), stride=(2, 1))

        mpool13_T = tf.transpose(a=mpool13, perm=[0,2,1,3])
        mpool13_T_RSH = tf.reshape(mpool13_T, [-1, self._fv, self._last_filters])
        return tf.reshape(mpool13_T_RSH, [-1, self._n_features])


# an activation function
class Activation_Function:
    def __init__(self, fn):
        self._fn = fn

    def call(self, features, alpha, name):
        return self._fn(features, alpha, name)

# a single convolutional layer
class Conv_Layer(tf.keras.layers.Layer):
    def __init__(self, input_layer, filter_in, filter_out, training, cfg):
        # inherit from the keras layer class
        super(conv_layer, self).__init__()

        # this is inherited from the keras layer and allows this to be train
	    self.trainable=True

        self._input_layer = input_layer
        self._filter_in = filter_in
        self._filter_out = filter_out
        self._training = training

        # generate a weight variable
		self._weight = weight_variable([3, 3, filter_in, filter_out])

        # if we don't want a sigmoid activation function
		if cfg.LeakyReLU:
			self._activation = Activation_Function(tf.nn.leaky_relu)

        else:
            self._activation = Activation_Function(tf.nn.relu)

    # compute a 2-dimensional convolution on this layer
    def conv2d(x, W, stride=(1, 1), padding='SAME'):
        return tf.nn.conv2d(
            input=x,
            filters=W,
            strides=[1, stride[0], stride[1], 1],
            padding=padding
        )

    def batch_norm_conv(self):
        pass

    # compute the next layer
    def activate(self):
        return self._activation(
            batch_norm_conv(conv2d(self._input_layer, self._weight),
                self._filter_out,
                self._training)
            )
