#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Mindaugas Greibus
This sample works with VAD branch http://svn.code.sf.net/p/cmusphinx/code/branches/feature-vad
'''

from pocketsphinx import Decoder
import time
from os import path
import pyaudio


CHUNK = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000



MODELDIR = "../models"
#MODELDIR = "/home/as/src/speech/sphinx/lt-pocketsphinx-tutorial/impl/models"

# Create a decoder with certain model
config = Decoder.default_config()
config.set_string('-hmm', path.join(MODELDIR, 'hmm/lt.cd_cont_200/'))
config.set_string('-jsgf', path.join(MODELDIR, 'lm/robotas.gram'))
config.set_string('-dict', path.join(MODELDIR, 'dict/robotas.dict'))
decoder = Decoder(config)


p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
#Indicate listening for next utterance
print ("READY....")

frames = []
cur_vad_state = 0;

decoder.start_utt(None)

while True:
    data = stream.read(CHUNK)
    time.sleep (0.100)
    #frames.append(data)
    decoder.process_raw(data, False, False)
    vad_state = decoder.get_vad_state()
    if vad_state and not cur_vad_state:
        #silence -> speech transition,
        #let user know that he is heard
        print("Listening...\n")
    if not vad_state and cur_vad_state:
        #speech -> silence transition,
        #time to start new utterance
        decoder.end_utt()
        # Retrieve hypothesis.
        hypothesis = decoder.hyp()
        if hypothesis is not None:
            print ('Best hypothesis: ', hypothesis.best_score, hypothesis.hypstr)
        decoder.start_utt(None)
        #Indicate listening for next utterance
        print ("READY....")
    cur_vad_state = vad_state
#close micraphone
stream.stop_stream()
stream.close()
p.terminate()
print("Ended...")



