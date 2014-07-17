'''
Created on Dec 29, 2013


@author: Mindaugas Greibus
'''
import sys, os
import subprocess
import select
import pty

MODELDIR = "../models"


params = ["pocketsphinx_continuous", "-inmic","yes" ,'-hmm', os.path.join(MODELDIR, 'hmm/lt.cd_cont_200/'),
              "-jsgf", os.path.join(MODELDIR, 'lm/robotas.gram'),
             "-dict", os.path.join(MODELDIR, 'dict/robotas.dict')]

sphinx_proc = subprocess.Popen(params,stdout=subprocess.PIPE, stderr=subprocess.PIPE , shell=False)

for line in iter(sphinx_proc.stdout.readline, ''):
    line = line.replace('\r', '').replace('\n', '')
    print ">: " + line
    sphinx_proc.stdout.flush()
