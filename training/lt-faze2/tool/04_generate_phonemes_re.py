#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Mindaugas Greibus
'''
import glob,os, re, chardet
import shutil
import subprocess
import transcriber



wordSet = set([])

src_dir = "../wav"
for corpus_dir in os.listdir(src_dir):
    if(os.path.isdir(os.path.join(src_dir, corpus_dir))):
       print corpus_dir
       with open(src_dir + "/../target/_"+ corpus_dir+"_word.txt", "rb") as infile:
            for line in infile:
                line = line.rstrip()
                line=line.replace("<sil>", "");
                wordSet.add(line)

wordSet.remove("")

wordList = sorted(list(wordSet))

wordsStr = "\n".join(wordList)
print ">>>> wordsStr\n" + wordsStr

#automagical transformation
transcriber = transcriber.Transcriber()

phonemeSet = set([])

with open("../target/liepa.dic", "wb") as outfile:
    for i in range(len(wordList)):
        key = wordList[i]
        value = transcriber.transcribe(key)

        phonemeSet.update(value.split(" "))
        #print key +"\t"+ value
        outfile.write(key +"\t"+ value + "\n")


with open("../target/liepa.phone", "wb") as outfile:
    outfile.write("SIL\n")
    for phone in sorted(phonemeSet):
        outfile.write(phone + "\n")