#!/bin/bash
# usage ./extract-word.sh


for corpusDir in $(find ./wav -mindepth 1 -maxdepth 1); do
	corpusDirName=$(basename ${corpusDir})
	echo "Processing $corpusDirName all textgrids"
	for fileName in $(find $corpusDir -name '*.Textgrid'); do
		awk -f extract-word.awk $fileName >> target/_lt_$corpusDirName.transcription
	done

	cat target/_lt_all-words.txt >> target/_lt_raw-words.txt
	mv target/_lt_all-words.txt target/_lt_$corpusDirName-words.txt
	mv target/_lt_all.fileids target/_lt_$corpusDirName.fileids

	smapleNumber=$(wc -l < target/_lt_$corpusDirName.transcription)
	testNumber=$(($smapleNumber/10))
	trainNumber=$(($smapleNumber-$testNumber))

	echo "splittng  $corpusDirName transcriptions and fileids to testing and taining sets"
	head -n $trainNumber target/_lt_$corpusDirName.transcription >> target/lt_train.transcription
	tail -n $testNumber target/_lt_$corpusDirName.transcription >> target/lt_test.transcription
	head -n $trainNumber target/_lt_$corpusDirName.fileids >> target/lt_train.fileids
	tail -n $testNumber target/_lt_$corpusDirName.fileids >> target/lt_test.fileids
done


echo "generating lt.dic"
awk -f ./make_ltdic.awk target/_lt_raw-words.txt >> target/_lt_all.dic

echo "sorting lt.dic and lt.phone"
echo "SIL">> "target/_lt_all.phone"
#cat lt_*.transcription >lt_all.transcription
sort -u -o target/lt.dic target/_lt_all.dic
#sed -i -e "1d" target/lt.phone
sort -u -o target/lt.phone target/_lt_all.phone

