#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: Mindaugas Greibus
'''
import glob,os, chardet,re
import itertools
import subprocess
import logging



#logging.basicConfig(filename='/tmp/liepa/extract_dict.log',level=logging.DEBUG)


def checkSpelling(text):
    text = text.replace("<sil>", "")
    cmd = "echo " +text + " | hunspell -i utf-8 -d lt_LT"
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result, err = p.communicate()
    if err:
        return err

    wordIssues = []

    if result:
        #print result
        for line in result.split("\n"):
            #print (line, re.search('& ([\wąčęėįšųūž]+) \d \d: ([\wąčęėįšųūž]+)', line))

            match = re.search('& ([\wąčęėįšųūž]+) \d+ \d+: ([\wąčęėįšųūž]+)', line)
            if not match is None:
                #print ("test",line, match.group(1).lower() != match.group(2).lower())
                if match.group(1).lower() != match.group(2).lower():
                    print "Spell issue: "+ line
                    wordIssues.append( match.group(1).lower() )
    #print text
    return wordIssues

def force_decode(string, codecs=['utf-16-le','windows-1257']):
    for i in codecs:
        try:
            decoded = string.decode(i)
            testEncode = decoded.encode('utf-8')
            #print testEncode
            #print ("Regexp: ", m.group(0))
            if re.search('[a-z]', testEncode) is not None:
                return decoded
        except:
            pass

    raise Exception("Not possible detect coding! " + string)
#     logging.warn("cannot decode url %s" % ([string]))



for corpus_dir in os.listdir("../wav"):
    contentMap = {}
    wordsSet = set([])
    print (corpus_dir)
    read_files = glob.glob("../wav/" + corpus_dir + "/*.txt")
    for in_file in read_files:
        with open(in_file, "rb") as infile:
            #print  in_file
            line = infile.read()
            # if fails use 'iconv -f  Windows-1257 -t utf-8 ../wav/S001/001_24-S003Mi.txt'
#             line = line.decode('windows-1257')
#             line = line.decode('utf-16-le')
            line = force_decode(line).replace(u"\ufeff", "")
            line = line.encode('utf-8')
            line = line.lower()
            line = line.replace("_tyla", " <sil> ");
            line = re.sub('[_\-]{1}\s*pauze'," <sil>", line)#pause could be written in multiple ways
            line = line.replace("_ikvepimas", " <sil> ");#should be breath
            line = line.replace("_iskvepimas", " <sil> ");#should be breath
            line = re.sub('_([\wąčęėįšųū])',"<sil> \g<1>", line, re.UNICODE)
            line = re.sub('(<sil>\s+)+'," <sil> ", line, re.UNICODE)#multi silences
            line = re.sub('^\s*<sil>\s+',"", line) #extra silence in front
            line = re.sub('\s*<sil>$',"", line)#extra silence in end
            line = re.sub('\s+'," ", line, re.UNICODE)

            if not re.search('_', line) is None:
                print "skiping. " + in_file
                logging.warning(',%s,has unexepcted _', in_file)
                continue;

            spellIssue = checkSpelling(line)
            if spellIssue:
                logging.warning(',%s, spelling issue: %s', in_file, "; ".join(spellIssue))
                continue


            wordList = line.split(' ')


            wordsSet.update(wordList)

            base_name = os.path.basename(in_file)
            contentMap[os.path.splitext(base_name)[0]] = line


    with open("../target/_"+corpus_dir+".transcription", "wb") as outfile:
        for key, value in contentMap.iteritems():
            out_line = "<s> {line} </s> ({file_name})".format(line=value,file_name=key)
            outfile.write(out_line + "\n")
            #print  out_line

    trainSize = len(contentMap)//10
    i = iter(contentMap.items())
    testMap = dict(itertools.islice(i, trainSize))
    trainMap = dict(i)

    with open("../target/_"+corpus_dir+"_test.transcription", "wb") as outfile:
        for key, value in testMap.iteritems():
            out_line = "<s> {line} </s> ({file_name})".format(line=value,file_name=key)
            outfile.write(out_line + "\n")

    with open("../target/_"+corpus_dir+"_train.transcription", "wb") as outfile:
        for key, value in trainMap.iteritems():
            out_line = "<s> {line} </s> ({file_name})".format(line=value,file_name=key)
            outfile.write(out_line + "\n")

    with open("../target/_"+corpus_dir+"_test.fileids", "wb") as outfile:
        for key, value in testMap.iteritems():
            outfile.write(corpus_dir +"/" + key + "\n")

    with open("../target/_"+corpus_dir+"_train.fileids", "wb") as outfile:
        for key, value in trainMap.iteritems():
            outfile.write(corpus_dir +"/" + key + "\n")

    #print wordsSet
    with open("../target/_"+corpus_dir+"_word.txt", 'wb') as outfile:
        for item in set(wordsSet):
            outfile.write(item+"\n")
