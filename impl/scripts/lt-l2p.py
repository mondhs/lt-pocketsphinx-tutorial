#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- build on est-l2p.py  https://github.com/alumae/et-pocketsphinx-tutorial
'''
Created on Jun 1, 2013

@author: mondhs
@author: tanel
'''

import sys
import re
import locale
import codecs

# Default settings based on the user's environment.
#locale.setlocale(locale.LC_ALL, '') 

l2p_rules = r"""

ch    X

ai    AI
au    AU
ei    EI
eu    EU
oi    OI
ui    UI
ie    IE
uo    UO
el    EL

a    A
ą    AA
b    B
c    C
č    CH
d    D
e    E
ę    EA
ė    EH
f    F
g    G
h    HH
i    IH
į    IY
y    IY
j    Y
k    K
l    L
m    M
n    N
o    OO
p    P
r    R
s    S
š    SH
t    T
u    UH
ų    UW
ū    UW
v    V
z    Z
ž    ZH




[\+-\?=~]    

"""

word_variants = u"""




"""

phon2phon = u"""
Š    SH
Ž    ZH
Č    CH
Ę    EA
Ė    EH
Ą    AA
"""


phones = u"A A1 AA AA1 AI AI2 AU AU1 AU2 B CH D E E1 EA EA2 EH EH1 EH2 EI EI2 EL EU F G IE IE1 IE2 IH IH1 IH2 IY IY1 IY2 K L L2 M M2 N N2 O OO P R R2 S SH SIL T UH UH1 UI UO UW UW1 V ww X Y Z ZH".split()

def is_phone(phone):
    return phone in phones


if __name__ == '__main__':
    #prepare rules
    rules = []
    for l in l2p_rules.splitlines():
        ss = l.split()
        if len(ss) > 0:
            if len(ss) == 1:
                rules.append((ss[0].decode('utf-8'), ""))
            else:
                rules.append((ss[0].decode('utf-8'), "".join([" ", ss[1].decode('utf-8')," "])))
        #print " ".join(ss)
    variant_rules = []
    for l in word_variants.splitlines():
        ss = l.split()
        if len(ss) > 1:
            variant_rules.append((ss[0], ss[1]))
    phon2phon_map = {}
    for l in phon2phon.splitlines():
        ss = l.split()
        if len(ss) > 1:
            phon2phon_map[ss[0]] = ss[1]
    # process jsgf
    encoding = locale.getdefaultlocale()[1]
    print >> sys.stderr, "Using", encoding , "for input and output"
    
    sys.stdout = codecs.getwriter(encoding)(sys.stdout);
    
    #read input stream
    for l in codecs.getreader(encoding)(sys.stdin):        
        ss = l.split()
        
        
        if len(ss) > 0:
            word = ss[0]
            word = re.sub(r".*\[(.*)\]", r"\1", word)
            word = word.lower()
            words = [word]
            for (fr, to) in variant_rules:
                new_word = re.sub(r"^" + fr + r"$", to, words[0])
                #print "".join(["word_variants: ", fr, " => ", to, " @ ", words[0], " = ", new_word])

                if new_word != words[0]:
                    words.append(new_word)
            
            for i in xrange(len(words)):
                word = words[i]
                phon = word
                for (fr, to) in rules:
                    new_phon = re.sub(fr, to, phon)
                    #print "".join(["l2p_rules: ", fr, " => ", to, " @ ", phon, " = ", new_phon])
                    phon = new_phon

                if i > 0:
                    print "%s(%d)" % (ss[0], (i+1)),
                else:
                    print ss[0],
                #filter out non phoneme symbols
                print " ".join(filter(is_phone, [phon2phon_map.get(p, p) for p in phon.split(" ")]))
                sys.stdout.flush()
         
        
