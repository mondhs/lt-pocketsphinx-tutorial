#!/bin/bash

text2wfreq < ../liepa_all.transcription | wfreq2vocab > target/liepa.vocab
text2idngram -vocab target/liepa.vocab  -idngram target/liepa.idngram < ../liepa_all.transcription
idngram2lm -vocab_type 0 -idngram target/liepa.idngram  -vocab target/liepa.vocab -arpa target/liepa.arpa
sphinx_lm_convert -i target/liepa.arpa -o ../liepa.lm.DMP
