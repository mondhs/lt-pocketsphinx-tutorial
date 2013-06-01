#!/bin/bash

mkdir wav-resample

#prename -n 's/^(.*).wav$/$1-DIR.wav/'  *.wav
#prename -n 's/^(.*).Textgrid$/$1-DIR.Textgrid/'  *.Textgrid

for fileFullName in $(find ./wav44 -name '*.wav'); do
  fileName=$(basename ${fileFullName})
  subdirName=`echo $(dirname ${fileFullName})|sed 's/^\.\/wav44\///g'`
  resampledDir=wav-resample/$subdirName
  mkdir -p $resampledDir
  sox $fileFullName -b 16 $resampledDir/$fileName rate 16000 dither -s
done

