'''
Created on Dec 29, 2013

@author: Mindaugas Greibus
'''

from pocketsphinx import Decoder
from os import environ, path
#from sphinxbase import *

MODELDIR = "../models"
#MODELDIR = "/home/as/src/speech/sphinx/lt-pocketsphinx-tutorial/impl/models"

# Create a decoder with certain model
config = Decoder.default_config()
config.set_string('-hmm', path.join(MODELDIR, 'hmm/lt.cd_cont_200/'))
config.set_string('-jsgf', path.join(MODELDIR, 'lm/robotas.gram'))
config.set_string('-dict', path.join(MODELDIR, 'dict/robotas.dict'))
decoder = Decoder(config)

decoder.decode_raw(open(path.join(MODELDIR, '../test/audio/varyk_pirmyn-16k.wav'), 'rb'))

# Retrieve hypothesis.
hypothesis = decoder.hyp()
print 'Best hypothesis: ', hypothesis.best_score, hypothesis.hypstr
print 'Best hypothesis segments: ', [seg.word for seg in decoder.seg()]


