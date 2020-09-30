"""
Auth: Nate Koike
Date: 28 September 2020
Desc: a generalized clone of the HandwritingRecognitionSystem_v2 developed by
      Edgar Chamas and his research associates in 2018
"""

# standard python imports
import tensorflow as tf
import sys
import os
import cv2
import numpy as np
import math

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
    # also store the length
    [charset, char_count] = load_list(charset_path)

    # # debugging code
    # print(charset)

    # get a list of all the image files
    img_lst  = load_list(img_list_path)[0]

    ####################################################################
    #CNN-specific architecture configuration
    ####################################################################
    WND_HEIGHT = 64 		#Extraction window height
    WND_WIDTH = 64			#Extraction window width
    WND_SHIFT = WND_WIDTH - 2	#Window shift

    MPoolLayers_ALL = 5	#Nbr of all maxpool layers
    MPoolLayers_H = 2	#Nbr of maxpool in horizontal dimension
    LastFilters = 512	#Nbr of feature maps at the last conv layer
    ####################################################################
