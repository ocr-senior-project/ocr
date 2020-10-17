"""
Auth: Nate Koike, Roger Danilek
Date: 16 October 2020
Desc: implement a class-based convolutional neural networks
"""

import tensorflow as tf
from settings import CFG

# a custom class for a convolutional neural network
class CNN:
    def __init__(self, cfg):
        self._cfg = cfg

    # perform max pooling to down-sample the input
    def max_pool(self, x, k_size=(2, 2), stride=(2, 2)):
        # x is a Conv_Layer object
        return tf.nn.max_pool2d(
            input = x.activate(),
            ksize = [1, k_size[0], k_size[1], 1],
            strides = [1, stride[0], stride[1], 1],
            padding = 'SAME')

    # build and run the cnn
    def build(self, x_in):
        with self._cfg as cfg:
            # x is a numpy array
            # create the hidden layers that make up the "black box" of our NN
            layer1 = Conv_Layer(x_in, 1, 64, cfg)
            layer2 = Conv_Layer(layer1, 64, 64, cfg)
            mpool2 = self.max_pool(layer2, ksize=(2,2), stride=(2,2))

            layer3 = Conv_Layer(mpool2, 64, 128, cfg)
            layer4 = Conv_Layer(layer3, 128, 128, cfg)
            mpool4 = self.max_pool(layer4, ksize=(2, 2), stride=(2, 2))

            layer5 = Conv_Layer(mpool4, 128, 256, cfg)
            layer6 = Conv_Layer(layer5, 256, 256, cfg)
            layer7 = Conv_Layer(layer6, 256, 256, cfg)
            mpool7 = self.max_pool(layer7, ksize=(2, 1), stride=(2, 1))

            layer8 = Conv_Layer(mpool7, 256, 512, cfg)
            layer9 = Conv_Layer(layer8, 512, 512, cfg)
            layer10 = Conv_Layer(layer9, 512, 512, cfg)
            mpool10 = self.max_pool(layer10, ksize=(2, 1), stride=(2, 1))

            layer11 = Conv_Layer(mpool10, 512, 512, cfg)
            layer12 = Conv_Layer(layer11, 512, 512, cfg)
            layer13 = Conv_Layer(layer12, 512, cfg.last_layer, cfg)
            mpool13 = self.max_pool(layer13, ksize=(2, 1), stride=(2, 1))

            mpool13_T = tf.transpose(a=mpool13, perm=[0,2,1,3])
            mpool13_T_RSH = tf.reshape(mpool13_T, [-1, cfg.fv, cfg.last_layer])

        return tf.reshape(mpool13_T_RSH, [-1, cfg.n_features])

# an activation function
class Activation_Function:
    def __init__(self, fn):
        self._fn = fn

    def call(self, features, alpha, name):
        return self._fn(features, alpha, name)

# a single convolutional layer
class Conv_Layer(tf.keras.layers.Layer):
    def __init__(self, input_layer, filter_in, filter_out, cfg, train=True):
        # inherit from the keras layer class
        super(conv_layer, self).__init__()

        self._input_layer = input_layer
        self._filter_in = filter_in
        self._filter_out = filter_out

        # decide whether this layer is trainable or not
        self.trainable = train

        # generate a weight variable
		self._weight = weight_variable([3, 3, filter_in, filter_out])

        # if we don't want a sigmoid activation function
		if cfg.LeakyReLU:
			self._activation = Activation_Function(tf.nn.leaky_relu)
        # if we do
        else:
            self._activation = Activation_Function(tf.nn.relu)

    # compute a 2-dimensional convolution on this layer
    def conv2d(x, weights, stride=(1, 1), padding='SAME'):
        return tf.nn.conv2d(
            input = x,
            filters = weights,
            strides = [1, stride[0], stride[1], 1],
            padding = padding)

    def batch_norm_conv(self):
        pass

    # cite: https://stackoverflow.com/questions/33949786/how-could-i-use-batch-normalization-in-tensorflow
    # deleted variable scope 'bn'
    def batch_norm_conv(self, x, n_out):
        offset = tf.Variable(tf.constant(0.0, shape=[n_out]), name='beta')
        scale = tf.Variable(tf.constant(1.0, shape=[n_out]), name='gamma')

        # compute the mean and variance of the batch in a global context
        batch_mean, batch_variance = tf.nn.moments(x, [0, 1, 2], name='moments')

        # maintain the moving averages of variables with an exponential decay
        ema = tf.train.ExponentialMovingAverage(0.5)

        # a closure to compute the mean variance
        def mean_var_with_update():
            # get an operation to update the moving dependencies
            ema_apply_op = ema.apply([batch_mean, batch_var])

            # ensure that the updating of moving dependencies runs first
            with tf.control_dependencies([ema_apply_op]):
                # return duplicates of the batch_mean and batch_variance tensors
                return tf.identity(batch_mean), tf.identity(batch_variance)

        # compute the global mean and variance
        mean, variance = tf.cond(
            self.trainable,
            true_fn=mean_var_with_update,
            false_fn=lambda: (ema.average(batch_mean), ema.average(batch_var)))

        # return the normalized, scaled, and offset tensor
        return tf.nn.batch_normalization(x, mean, variance, offset, scale, 1e-3)

    # compute the number going to the next layer
    def activate(self):
        return self._activation(
            self.batch_norm_conv(conv2d(self._input_layer, self._weight),
                self._filter_out,
                self._training))
