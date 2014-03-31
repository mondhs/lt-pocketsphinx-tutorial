#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Mindaugas Greibus
'''
import glob,os, re
import shutil
import subprocess
import logging


logging.basicConfig(filename='/tmp/liepa/transform_files.log',level=logging.DEBUG)

# coruptedFileSet = set(line.strip() for line in open('corupted_files.txt'))

#src_dir = "../wav22"
src_dir = "/home/mgreibus/tmp/3etapas_Garsynas"
dest_dir = "../wav"
fileFromatRegeExp = re.compile('([\w\d]+)_(\d+_[\d\w]+)')
for speak_dir in os.listdir(src_dir):
    for corpus_dir in os.listdir(os.path.join(src_dir, speak_dir)):
        if not corpus_dir.startswith("S"):
            print "Skiping: " + corpus_dir
            continue
        print (speak_dir, corpus_dir)
        #os.makedirs (dest_dir + "/" + corpus_dir)
        read_files = glob.glob(src_dir + "/" + speak_dir + "/"  + corpus_dir + "/*.wav")
        for wav_file in read_files:
            baseName = os.path.basename(wav_file)
            baseName = os.path.splitext(baseName)[0]
            txt_file = os.path.join(src_dir, speak_dir, corpus_dir, baseName+".txt")
            replaceName = fileFromatRegeExp.sub(r'\2-\1', baseName)
            speaker = ""
            try:
                speaker = fileFromatRegeExp.match(baseName).group(1)
            except:
                print "skipping. Not possible parse!" + wav_file
                continue
            wav_speaker_dir = os.path.join(dest_dir, speaker)
            dstWavfile = os.path.join(wav_speaker_dir, replaceName + ".wav")
            dstTxtfile = os.path.join(wav_speaker_dir, replaceName + ".txt")

            if not os.path.isfile(txt_file):
                logging.warning(',%s,%s', txt_file, 'txt file not exists')
                continue
            if os.path.getsize(wav_file) < 80000:
                logging.warning(',%s,%s: %d bytes', txt_file, 'too small txt', os.path.getsize(wav_file))
                continue
#             if baseName in coruptedFileSet:
#                 logging.warning(',%s,%s', baseName, 'corupted')
#                 print "skipping. corrupted " + baseName
#                 continue

            try:
                os.makedirs(wav_speaker_dir)
            except OSError:
                if not os.path.isdir(wav_speaker_dir):
                    raise


#             print  (wav_file,dstWavfile)
            cmd = "sox  "+wav_file+" -b16 " +dstWavfile+ " rate 16000 dither -s"
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            result, err = p.communicate()
            if err:
                logging.warning(',%s,resampling issue: %s', baseName, err)
                continue
            shutil.copy2(txt_file, dstTxtfile)


