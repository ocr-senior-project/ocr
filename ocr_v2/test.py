"""
Auth: Roger Danilek, Nate Koike
Date: 22 October 2020
Desc: use a class-based neural net to perform ocr
"""
import tensorflow as tf
from PIL import Image
import datetime
import os
import math

tf.compat.v1.disable_eager_execution()

import cnn
import rnn
import settings

def LoadModel(session, path):
    saver = tf.compat.v1.train.Saver()
    ckpt = tf.train.get_checkpoint_state(path)

    if ckpt and ckpt.model_checkpoint_path:
        saver.restore(session, ckpt.model_checkpoint_path)
        print('Checkpoint restored')
    else:
        print('No checkpoint found')
        exit()

# process a single string
def run(cfg, img):
    print('TESTING')

    # idk what this is but were rolling with it
    vec_per_win = cfg.width / math.pow(2, cfg.h_maxpool_layers)

    # save the image to a temporary file
    img_fname = str(datetime.datetime.now())[-6:] + ".png"
    img.save(img_fname)

    # blank image placeholder
    x = tf.compat.v1.placeholder(tf.float32, shape=[None, cfg.height, cfg.width])

    # Create a blank array for 1 output?
    seq_lens = tf.compat.v1.placeholder(tf.int32, shape=[1])

    # insert a fourth dimension at the end of the tensor
    x_expanded = tf.expand_dims(x, 3)

    session = tf.compat.v1.Session()
    session.run(tf.compat.v1.global_variables_initializer())

    LoadModel(session, cfg.save_dir + '/')

    print("#################")
    tf.print(x_expanded)
    print("#################")

    # create the inputs for the rnn
    ins = cnn.CNN(cfg).build(x_expanded)

    # get the raw prediction for one character
    logits = RNN(ins, seq_lens, 'RNN')

    # decode prediction string from the probability map (logits)
    decoded, _ = tf.nn.ctc_beam_search_decoder(logits, seq_lens)

    session.run(tf.compat.v1.assign(phase_train, False))

    # create a dictionary for the tf session
    feed = {x: [img_fname], SeqLens: seq_lens}

    Decoded = session.run([decoded], feed_dict=feed)[0]

    trans = session.run(tf.sparse.to_dense(Decoded[0]))

    decodedStr = ""

    for i in range(0, len(trans[0])):
        if trans[0][i] == 0:
            if (i != (len(trans[0]) - 1)):
                if trans[0][i + 1] == 0:
                    break
                else:
                    decodedStr += Classes[trans[0][i]]

        else:
            if trans[0][i] == (NClasses - 2):
                if (i != 0):
                    decodedStr += ' '
            else:
                decodedStr += Classes[trans[0][i]]

    decodedStr = decodedStr.replace("<SPACE>", " ")

    os.remove(img_fname)

    return decodedStr

def main():
    # get a cfg object
    cfg = settings.CFG(
        "charset.lst",
        "MATRICULAmodel",
        "MATRICULAmodel.ckpt",
        "log.txt",
        0,
        5,
        2,
        512)

    img = Image.open("img.png")

    run(cfg, img)

if __name__ == "__main__":
    main()

# from ocr_v2 import ocr

# out = open("out.txt", "w")
# charset = "charset.lst"
# img_lst = ""
# img_dir = ""
# model_dir = ""


# ocr(out, charset, img_lst, img_dir, model_dir)
