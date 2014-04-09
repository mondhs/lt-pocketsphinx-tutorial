#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Mindaugas Greibus
'''
import glob,os, re, chardet
import shutil
import subprocess


#subprocess.call("wine transcribe.exe 2000000 0 0 /tmp/test_word.txt", shell=True)


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

p = subprocess.Popen(['wine','transcribe.exe', '2000000', '0', '0' , '-', '-'], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
phonemerStr = p.communicate(input=wordsStr.decode('utf-8').encode("windows-1257"))[0]
print ">>>> phonemerStr\n" + phonemerStr

phonemerStr = re.sub("(['\s])\r\n","\g<1>", phonemerStr)
values = phonemerStr.split('\r\n')

phonemeSet = set([])

with open("../target/liepa.dic", "wb") as outfile:
    for i in range(len(wordList)):
        key = wordList[i]
        value = values[i]
        value=value.replace("_+", "");
        value=value.replace("+_", "");
        value=value.replace("'", "");
        value=value.replace("-", " ");
        value=value.replace("A", "a1");
        value=value.replace("E", "e1");
        value=value.replace("I", "i1");
        value=value.replace("J", "j1");
        value=value.replace("L", "l1");
        value=value.replace("M", "m1");
        value=value.replace("N", "n1");
        value=value.replace("O", "o1");
        value=value.replace("R", "r1");
        value=value.replace("S", "s1");
        value=value.replace("U", "u1");
        value=value.replace("W", "w1");
        value=value.replace("Z", "z1");


        phonemeSet.update(value.split(" "))
        #print key +"\t"+ value
        outfile.write(key +"\t"+ value + "\n")


with open("../target/liepa.phone", "wb") as outfile:
    outfile.write("SIL\n")
    for phone in sorted(phonemeSet):
        outfile.write(phone + "\n")