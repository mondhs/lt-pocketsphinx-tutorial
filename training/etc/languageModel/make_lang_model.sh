#!/bin/bash

text2wfreq < lt_all.transcription | wfreq2vocab > target/lt.vocab
text2idngram -vocab target/lt.vocab  -idngram target/lt.idngram <lt_all.transcription
idngram2lm -vocab_type 0 -idngram target/lt.idngram  -vocab target/lt.vocab -arpa target/lt.arpa
sphinx_lm_convert -i target/lt.arpa -o lt.lm.DMP
