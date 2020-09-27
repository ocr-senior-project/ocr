###
# Copyright 2018 Edgard Chammas. All Rights Reserved.
# Licensed under the Creative Commons Attribution-NonCommercial International
# Public License, Version 4.0.
# You may obtain a copy of the License at
# https://creativecommons.org/licenses/by-nc/4.0/legalcode
###

#!/usr/bin/python

"""
Auth: Nate Koike
Date: 26 September 2020
Desc: the ocr test file, but as a module with more parameters instead of hard
	  coded values
"""

# standard python imports
import tensorflow as tf
import sys
import os
import cv2
import numpy as np
import codecs
import math

# ocr package imports
from HandwritingRecognitionSystem_v2.config import cfg
from HandwritingRecognitionSystem_v2.util import LoadClasses
from HandwritingRecognitionSystem_v2.util import LoadModel
from HandwritingRecognitionSystem_v2.util import ReadData
from HandwritingRecognitionSystem_v2.util import LoadList
from HandwritingRecognitionSystem_v2.cnn import CNN
from HandwritingRecognitionSystem_v2.cnn import WND_HEIGHT
from HandwritingRecognitionSystem_v2.cnn import WND_WIDTH
from HandwritingRecognitionSystem_v2.cnn import MPoolLayers_H
from HandwritingRecognitionSystem_v2.rnn import RNN

# the wrapper for the test code
def ocr(output, charset_path, img_list_path, img_dir, model_dir):
    """
           output: the file where we will write the transcription
     charset_path: the path to the file containing all the usable characters
    img_list_path: the path to the file containing the filename of every image
                   without its file extension
          img_dir: the path to the directory containing all the image files
        model_dir: the path to the directory containing the trained neural
                   network model
    """

    # get a list of all the characters that are usable in the text
    Classes = LoadClasses(charset_path)

    # the number of characters available to use
    NClasses = len(Classes)

    # img_list_path is the path of a file with the filenames of all the images
    # minus the file extension
    FilesList = LoadList(img_list_path)

    # magic code from the initial repo
    WND_SHIFT = WND_WIDTH - 2
    VEC_PER_WND = WND_WIDTH / math.pow(2, MPoolLayers_H)
    phase_train = tf.Variable(True, name='phase_train')

    # more magic code
    x = tf.compat.v1.placeholder(
		tf.float32,
		shape=[None, WND_HEIGHT, WND_WIDTH])

    # look! magic code!
    SeqLens = tf.compat.v1.placeholder(shape=[cfg.BatchSize], dtype=tf.int32)

    # do you believe in magic...
    x_expanded = tf.expand_dims(x, 3)

    # in a young girl's heart?
    Inputs = CNN(x_expanded, phase_train, 'CNN_1')

    # how the music can free her, whenever it starts
    logits = RNN(Inputs, SeqLens, 'RNN_1')

    # CTC Beam Search Decoder to decode pred string from the prob map
    decoded, log_prob = tf.nn.ctc_beam_search_decoder(
		inputs=logits,
		sequence_length=SeqLens)

    #Reading test data...
    InputListTest, SeqLensTest, _ = ReadData(
        img_dir, # the path to the directory containing the line image files
		img_list_path,
		len(FilesLists), # look at all the files, not just some of them
		WND_HEIGHT, # magic...
		WND_WIDTH, # numbers...
		WND_SHIFT, # wee!!!
		VEC_PER_WND) # woo!!!

    # happy startup noises
    print('Initializing...')

    # start a session, i guess
    session = tf.compat.v1.Session()
    session.run(tf.compat.v1.global_variables_initializer())

    # load the model from the place where the model is
    LoadModel(session, model_dir+'/')

    # under normal circumstances...
    try:
        # run a session, i guess?
        session.run(tf.compat.v1.assign(phase_train, False))

        # magic code wee
        randIxs = range(0, len(InputListTest))

        # magic numbers too? WOAH
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
                            else: decodedStr = "%s%s" % \
                                (decodedStr, Classes[trans[i][j]])
                        else:
                            break
                    else:
                        if trans[i][j] == (NClasses - 2):
                            if (j != 0): decodedStr = "%s " % (decodedStr)
                            else: continue
                        else:
                            decodedStr = "%s%s" % \
                                (decodedStr, Classes[trans[i][j]])

                decodedStr = decodedStr.replace("<SPACE>", " ")
                decodedStr = decodedStr[:] + "\n"

                # remove the filename since thats ugly
                output.write(decodedStr.split(' ')[1:].join(' '))

            start += cfg.BatchSize
            end += cfg.BatchSize
            batch += 1
    # close gracefully
    except (KeyboardInterrupt, SystemExit, Exception) as e:
        print("[Error/Interruption] %s" % str(e))
        print("Clossing TF Session...")
        session.close()
        print("Terminating Program...")
        sys.exit(0)
