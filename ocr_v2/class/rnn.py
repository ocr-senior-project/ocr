"""
Auth: Nate Koike
Date: 16 October 2020
Desc: implement a class-based convolutional neural networks
"""

import tensorflow as tf
import numpy as np
import math
from settings import CFG

class RNN():
    def __init__(self, inputs, seq_lens, cfg):
        self._cfg = cfg

        # ----------------------------------------------------------------------
		# ---------------- Construct Batch Sequences for LSTM ------------------
        # ----------------------------------------------------------------------
		maxLen = tf.reduce_max(input_tensor=seq_lens, axis=0)

		n, offset = 0, 0

		ndxs = tf.reshape(tf.range(seq_lens[0]), [seq_lens[n], 1])
		res = tf.reshape(tf.gather_nd(inputs, [ndxs]), [-1])
		zero_padding = tf.zeros([NFeatures * maxLen] - tf.shape(input=res), dtype=res.dtype)
		a_padded = tf.concat([res, zero_padding], 0)
		result = tf.reshape(a_padded, [maxLen, NFeatures])
		inputs2 = result

		for n in range(1, cfg.BatchSize):
			offset = tf.cumsum(seq_lens)[n-1]
			ndxs = tf.reshape(tf.range(offset, seq_lens[n]+offset), [seq_lens[n], 1])
			res = tf.gather_nd(inputs, [ndxs])
			res = tf.reshape(res, [-1])
			zero_padding = tf.zeros([NFeatures * maxLen] - tf.shape(input=res), dtype=res.dtype)
			a_padded = tf.concat([res, zero_padding], 0)
			result = tf.reshape(a_padded, [maxLen, NFeatures])
			inputs2 = tf.concat([inputs2, result], 0)

		n = 0
		ndxs = tf.reshape(tf.range(n, cfg.BatchSize * maxLen, maxLen), [cfg.BatchSize, 1])
		inputs = tf.gather_nd(inputs2, [ndxs])

		i = tf.constant(1)

		def condition(i, prev): return tf.less(i, maxLen)

		def body(i, prev):
			ndxs = tf.reshape(tf.range(i, cfg.BatchSize * maxLen, maxLen), [cfg.BatchSize, 1])
			result = tf.gather_nd(inputs2, [ndxs])
			next = tf.concat([prev, result], 0)
			return [tf.add(i, 1), next]

		i, inputs = tf.while_loop(cond=condition, body=body, loop_vars=[i, inputs], shape_invariants=[i.get_shape(), tf.TensorShape([None, cfg.BatchSize, NFeatures])])

		###############################################################
		#Construct LSTM layers

		initializer = tf.compat.v1.keras.initializers.VarianceScaling(scale=1.0, mode="fan_avg", distribution="uniform")

		stacked_rnn_forward = []
		for i in range(cfg.NLayers):
			stacked_rnn_forward.append(tf.compat.v1.nn.rnn_cell.LSTMCell(num_units=cfg.NUnits, initializer=initializer, use_peepholes=True, state_is_tuple=True))
		forward = tf.compat.v1.nn.rnn_cell.MultiRNNCell(stacked_rnn_forward, state_is_tuple=True)

		stacked_rnn_backward = []
		for i in range(cfg.NLayers):
			stacked_rnn_backward.append(tf.compat.v1.nn.rnn_cell.LSTMCell(num_units=cfg.NUnits, initializer=initializer, use_peepholes=True, state_is_tuple=True))
		backward = tf.compat.v1.nn.rnn_cell.MultiRNNCell(stacked_rnn_backward, state_is_tuple=True)

		[fw_out, bw_out], _ = tf.compat.v1.nn.bidirectional_dynamic_rnn(cell_fw=forward, cell_bw=backward, inputs=inputs, time_major=True, dtype=tf.float32,sequence_length=tf.cast(seq_lens, tf.int64))

		# Reshaping forward, and backward outputs for affine transformation
		fw_out = tf.reshape(fw_out,[-1, cfg.NUnits])
		bw_out = tf.reshape(bw_out,[-1, cfg.NUnits])

		# Linear Layer params
		W_fw = tf.Variable(tf.random.truncated_normal(shape=[cfg.NUnits, NClasses], stddev=np.sqrt(2.0 / cfg.NUnits), dtype=tf.float32), dtype=tf.float32)
		W_bw = tf.Variable(tf.random.truncated_normal(shape=[cfg.NUnits, NClasses], stddev=np.sqrt(2.0 / cfg.NUnits), dtype=tf.float32), dtype=tf.float32)
		b_out = tf.constant(0.1,shape=[NClasses], dtype=tf.float32)

		# Perform an affine transformation
		logits =  tf.add( tf.add( tf.matmul(fw_out,W_fw), tf.matmul(bw_out,W_bw) ), b_out )

    def call(self):
		return tf.reshape(self._logits, [-1, self._cfg.batch_size, NClasses])
