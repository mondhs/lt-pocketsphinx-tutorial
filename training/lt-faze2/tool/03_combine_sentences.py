#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Mindaugas Greibus
'''
import glob,os, re, chardet
import shutil
import subprocess




wordSet = set([])

src_dir = "../wav"
with open("../target/liepa_test.fileids", "wb") as outfile:
    for corpus_dir in os.listdir(src_dir):
        if(os.path.isdir(os.path.join(src_dir, corpus_dir))):
           with open(src_dir + "/../target/_"+ corpus_dir+"_test.fileids", "rb") as infile:
                for line in infile:
                    outfile.write(line)

with open("../target/liepa_train.fileids", "wb") as outfile:
    for corpus_dir in os.listdir(src_dir):
        if(os.path.isdir(os.path.join(src_dir, corpus_dir))):
           with open(src_dir + "/../target/_"+ corpus_dir+"_train.fileids", "rb") as infile:
                for line in infile:
                    outfile.write(line)

with open("../target/liepa_test.transcription", "wb") as outfile:
    for corpus_dir in os.listdir(src_dir):
        if(os.path.isdir(os.path.join(src_dir, corpus_dir))):
           with open(src_dir + "/../target/_"+ corpus_dir+"_test.transcription", "rb") as infile:
                for line in infile:
                    outfile.write(line)

with open("../target/liepa_train.transcription", "wb") as outfile:
    for corpus_dir in os.listdir(src_dir):
        if(os.path.isdir(os.path.join(src_dir, corpus_dir))):
           with open(src_dir + "/../target/_"+ corpus_dir+"_train.transcription", "rb") as infile:
                for line in infile:
                    outfile.write(line)


with open("../target/liepa_all.transcription", "wb") as outfile:
    for corpus_dir in os.listdir(src_dir):
        if(os.path.isdir(os.path.join(src_dir, corpus_dir))):
           with open(src_dir + "/../target/_"+ corpus_dir+"_test.transcription", "rb") as infile:
                for line in infile:
                    outfile.write(line)
    for corpus_dir in os.listdir(src_dir):
        if(os.path.isdir(os.path.join(src_dir, corpus_dir))):
           with open(src_dir + "/../target/_"+ corpus_dir+"_train.transcription", "rb") as infile:
                for line in infile:
                    outfile.write(line)