'''
Created on Jul 17, 2014

Patch required:

svn diff pocketsphinx
Index: pocketsphinx/src/programs/continuous.c
===================================================================
--- pocketsphinx/src/programs/continuous.c	(revision 12538)
+++ pocketsphinx/src/programs/continuous.c	(working copy)
@@ -256,6 +256,8 @@
 main(int argc, char *argv[])
 {
     char const *cfg;
+ 
+    setvbuf(stdout, (char *) NULL, _IOLBF, 0); /* make line buffered stdout */
 
     config = cmd_ln_parse_r(NULL, cont_args_def, argc, argv, TRUE);


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
