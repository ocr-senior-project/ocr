"""
Auth: Nate Koike
Date: 16 October 2020
Desc: implement a class-based convolutional neural networks
"""

import tensorflow as tf
import numpy as np
import math
import settings

# a custom class for a recurrent neural network
class RNN:
    def __init__(self, inputs, seq_lens, cfg):
        self._cfg = cfg

        # ----------------------------------------------------------------------
        # ---------------- Construct Batch Sequences for LSTM ------------------
        # ----------------------------------------------------------------------
        # compute the maximum tensor value across the 0 axis of the sequence
        maxLen = tf.math.reduce_max(seq_lens, axis=0)

        # create a very tall tensor containing consecutive numbers for
        # everything in the sequence
        ndxs = tf.reshape(tf.range(seq_lens[0]), [seq_lens[0], 1])

        # get the first seq_lens[0] number of tensors from the input
        first_n = tf.gather_nd(inputs, [ndxs])

        # coerce the first n-tensors into being a list of numbers
        res = tf.reshape(first_n, [-1])

        # get a large number of 0's
        zero_padding = tf.zeros([cfg.n_features * maxLen] - tf.shape(res))

        # concatenate the list of numbers from earlier with the 0's
        a_padded = tf.concat([res, zero_padding], 0)

        # reshape the padded tensor into something more useful
        shaped_pad = tf.reshape(a_padded, [maxLen, NFeatures])

        # progrssively sum and pad the input across its entirety (i think)
        for n in range(1, cfg.BatchSize):
            # get the sum of all tensors along axis 0
            offset = tf.math.cumsum(seq_lens)[n-1]

            # create a very tall tensor containing consecutive numbers
            ndxs = tf.reshape(
                tf.range(offset, seq_lens[n] + offset),
                [seq_lens[n], 1])

            # sum the tensors in sequence[n] along axis 0 and coerce that into
            # being a list of numbers
            res = tf.reshape(tf.gather_nd(inputs, [ndxs]), [-1])

            # pad the input
            zero_padding = tf.zeros([NFeatures * maxLen] - tf.shape(res))
            a_padded = tf.concat([res, zero_padding], 0)
            result = tf.reshape(a_padded, [maxLen, NFeatures])
            shaped_pad = tf.concat([shaped_pad, result], 0)

        # create a tall tensor containing every maxLen-th number
        ndxs = tf.reshape(
            tf.range(0, cfg.batch_size * maxLen, maxLen),
            [cfg.batch_size, 1])

        # take only select padded inputs
        inputs = tf.gather_nd(shaped_pad, [ndxs])

        # now we need to progressively shape the input in a while loop
        # the condition of a tensorflow while loop
        def condition(i, prev): return tf.less(i, maxLen)

        # the body of a tensorflow while loop
        # progressively reshape forward an count the number of iterations
        def body(i, prev):
            ndxs = tf.reshape(
                tf.range(i, cfg.BatchSize * maxLen, maxLen),
                [cfg.BatchSize, 1])

            result = tf.gather_nd(shaped_pad, [ndxs])
            next = tf.concat([prev, result], 0)

            return [tf.add(i, 1), next]

        # progressively reshape the input and collect this reshaped input
        # we don't care about the number of iterations, so we can toss that
        _, inputs = tf.while_loop(
            condition,
            body,
            [tf.constant(1), inputs],
            shape_invariants=[
                i.get_shape(),
                tf.TensorShape([None, cfg.batch_size, cfg.n_eatures])
            ])

        ###############################################################
        #Construct LSTM layers

        # initialize with variance scaling
        initializer = tf.keras.initializers.VarianceScaling(
            mode="fan_avg",
            distribution="uniform")

        stacked_rnn_forward = []
        for i in range(cfg.n_layers):
            stacked_rnn_forward.append(
                tf.compat.v1.nn.rnn_cell.LSTMCell(
                    num_units=cfg.NUnits,
                    initializer=initializer,
                    use_peepholes=True,
                    state_is_tuple=True)
                )

        forward = tf.compat.v1.nn.rnn_cell.MultiRNNCell(stacked_rnn_forward, state_is_tuple=True)

        backwards_stack = []
        for i in range(cfg.n_layers):
            backwards_stack.append(
                tf.compat.v1.nn.rnn_cell.LSTMCell(
                    num_units=cfg.NUnits,
                    initializer=initializer,
                    use_peepholes=True,
                    state_is_tuple=True)
                )

        backward = tf.compat.v1.nn.rnn_cell.MultiRNNCell(backwards_stack, state_is_tuple=True)

        [fw_out, bw_out], _ = tf.compat.v1.nn.bidirectional_dynamic_rnn(cell_fw=forward, cell_bw=backward, inputs=inputs, time_major=True, dtype=tf.float32,sequence_length=tf.cast(seq_lens, tf.int64))

        # Reshaping forward, and backward outputs for affine transformation
        self._fw_out = tf.reshape(fw_out,[-1, cfg.n_units])
        self._bw_out = tf.reshape(bw_out,[-1, cfg.n_units])

        # Linear Layer params
        self._w_fw = tf.Variable(tf.random.truncated_normal(shape=[cfg.n_units, cfg.n_chars], stddev=np.sqrt(2.0 / cfg.NUnits), dtype=tf.float32), dtype=tf.float32)
        self._w_bw = tf.Variable(tf.random.truncated_normal(shape=[cfg.n_units, cfg.n_chars], stddev=np.sqrt(2.0 / cfg.NUnits), dtype=tf.float32), dtype=tf.float32)
        self._b_out = tf.constant(0.1,shape=[NClasses], dtype=tf.float32)

    def call(self):
        with self._cfg as cfg:
            # Perform an affine transformation
            logits = tf.add(
                tf.add(
                    tf.matmul(self._fw_out, self._w_fw),
                    tf.matmul(self._bw_out, self._w_bw)),
                b_out)

            # reshape the tensor (we only have 1 image so the second place is 1)
            return tf.reshape(logits, [-1, 1, cfg.n_chars])
