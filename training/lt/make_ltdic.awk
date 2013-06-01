#!/usr/bin/awk -f
#./make_ltdic.awk lt_all_words.txt
BEGIN {
}
{

    WordCount[$2]++
    WordHuman[$2]=$1
    phonemes = $2

    # remove punctuation and remove capital cases as this makes transformation complicated
    phonemes = gensub(/['\.]/,"","g",phonemes);
    phonemes = gensub(/O/,"o0","g",phonemes);
    phonemes = gensub(/N/,"n0","g",phonemes);
    phonemes = gensub(/Z/," ZH ","g",phonemes);
    phonemes = gensub(/tS/," CH ","g",phonemes);


    phonemes = gensub(/\^ai/," AI2 ","g",phonemes);
    phonemes = gensub(/\"\"ai/," AI2 ","g",phonemes);
    phonemes = gensub(/ai/," AI ","g",phonemes);
    phonemes = gensub(/\"\"au/," AU1 ","g",phonemes);
    phonemes = gensub(/\^au/," AU2 ","g",phonemes);
    phonemes = gensub(/au/," AU ","g",phonemes);
    phonemes = gensub(/\"\"ei/," EI ","g",phonemes);
    phonemes = gensub(/\^ei/," EI2 ","g",phonemes);
    phonemes = gensub(/ei/," EI ","g",phonemes);
    phonemes = gensub(/\^eu/," EU ","g",phonemes);
    phonemes = gensub(/\"\"eu/," EU ","g",phonemes);
    phonemes = gensub(/eu/," EU ","g",phonemes);
    phonemes = gensub(/oi/," OI ","g",phonemes);
    phonemes = gensub(/\"\"ui/," UI ","g",phonemes);
    phonemes = gensub(/\^ui/," UI ","g",phonemes);
    phonemes = gensub(/ui/," UI ","g",phonemes);
    phonemes = gensub(/\"\"ie/," IE1 ","g",phonemes);
    phonemes = gensub(/\^ie/," IE2 ","g",phonemes);
    phonemes = gensub(/ie/," IE ","g",phonemes);

    phonemes = gensub(/\^uo/," UO ","g",phonemes);    
    phonemes = gensub(/\"\"uo/," UO ","g",phonemes);
    phonemes = gensub(/uo/," UO ","g",phonemes);

    phonemes = gensub(/\"\"el/," EL ","g",phonemes);
    phonemes = gensub(/\el/," EL ","g",phonemes);







    phonemes = gensub(/\^a\:/," AA1 ","g",phonemes);
    phonemes = gensub(/\"\"a\:/," AA1 ","g",phonemes);
    phonemes = gensub(/a\:/," AA ","g",phonemes);


    phonemes = gensub(/\"\"i\:/," IY1 ","g",phonemes);
    phonemes = gensub(/\^i\:/," IY2 ","g",phonemes);
    phonemes = gensub(/i\:/," IY ","g",phonemes);


    phonemes = gensub(/\^o\:/," OO ","g",phonemes);
    phonemes = gensub(/\"\"o\:/," OO ","g",phonemes);
    phonemes = gensub(/o\:/," OO ","g",phonemes);

    phonemes = gensub(/\^E\:/," EH2 ","g",phonemes);
    phonemes = gensub(/\"\"E\:/," EH1 ","g",phonemes);
    phonemes = gensub(/E\:/," EH ","g",phonemes);
    phonemes = gensub(/\^e\:/," EA2 ","g",phonemes);
    phonemes = gensub(/\"\"e\:/," EA ","g",phonemes);
    phonemes = gensub(/e\:/," EA ","g",phonemes);

    phonemes = gensub(/\"\"u\:/," UW1 ","g",phonemes);
    phonemes = gensub(/\^u\:/," UW1 ","g",phonemes);
    phonemes = gensub(/u\:/," UW ","g",phonemes);

    #rest stuff
    phonemes = gensub(/\"\"a/," A1 ","g",phonemes);
    phonemes = gensub(/a/," A ","g",phonemes);
    phonemes = gensub(/b/," B ","g",phonemes);
    phonemes = gensub(/c/," C ","g",phonemes);
    phonemes = gensub(/d/," D ","g",phonemes);
    phonemes = gensub(/\"\"e/," E1 ","g",phonemes);
    phonemes = gensub(/e/," E ","g",phonemes);
    phonemes = gensub(/f/," F ","g",phonemes);
    phonemes = gensub(/g/," G ","g",phonemes);
    phonemes = gensub(/h/," HH ","g",phonemes);
    phonemes = gensub(/\"\"i/," IH1 ","g",phonemes);
    phonemes = gensub(/\^i/," IH2 ","g",phonemes);
    phonemes = gensub(/i/," IH ","g",phonemes);
    phonemes = gensub(/j/," Y ","g",phonemes);
    phonemes = gensub(/k/," K ","g",phonemes);
    phonemes = gensub(/\^l/," L2 ","g",phonemes);
    phonemes = gensub(/l/," L ","g",phonemes);
    phonemes = gensub(/\^m/," M2 ","g",phonemes);
    phonemes = gensub(/m/," M ","g",phonemes);
    phonemes = gensub(/\^n0/," N2 ","g",phonemes);
    phonemes = gensub(/n0/," N2 ","g",phonemes);
    phonemes = gensub(/\^n/," N2 ","g",phonemes);
    phonemes = gensub(/n/," N ","g",phonemes);
    phonemes = gensub(/\"\"o0/," O ","g",phonemes);
    phonemes = gensub(/o0/," O ","g",phonemes);
    phonemes = gensub(/p/," P ","g",phonemes);
    phonemes = gensub(/\^r/," R2 ","g",phonemes);
    phonemes = gensub(/r/," R ","g",phonemes);
    phonemes = gensub(/S/," SH ","g",phonemes);
    phonemes = gensub(/s/," S ","g",phonemes);
    phonemes = gensub(/t/," T ","g",phonemes);
    phonemes = gensub(/\"\"u/," UH1 ","g",phonemes);
    phonemes = gensub(/u/," UH ","g",phonemes);
    phonemes = gensub(/v/," V ","g",phonemes);
    phonemes = gensub(/z/," Z ","g",phonemes);
    phonemes = gensub(/x/," X ","g",phonemes);

    phonemes = gensub(/  /," ","g",phonemes);

    split(phonemes,phonemeList," ")
    for (iPhoneme in phonemeList){
      phonemeMap[phonemeList[iPhoneme]]++;
    }

    WordPhoneme[$2]=phonemes
}
END{
	for (var in WordCount){
		WordHumanCount[WordHuman[var]]++
		if (WordHumanCount[WordHuman[var]]>1){
			uniqueWord=WordHuman[var] "(" WordHumanCount[WordHuman[var]] ")"
		}else{
			uniqueWord=WordHuman[var]
		}
		#printf ("%-19s\t%d\t%-30s\t%-30s\n", WordHuman[var], WordHumanCount[WordHuman[var]], WordPhoneme[var], var) | "sort -k2 -n -r"
		printf ("%-19s %s\n", uniqueWord,  WordPhoneme[var], var) | "sort -k1 "
	}

	for (iPhonemem in phonemeMap){
		#print iPhonemem,"\t",phonemeMap[iPhonemem]>> "lt_phonemes.txt"
		print iPhonemem>> "target/_lt_all.phone"
	}
}

