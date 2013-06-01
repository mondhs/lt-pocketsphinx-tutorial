BEGIN {
	printf  ( "<s> ");
}

{
  if ($0 ~ /^[\t ]*name = /) {
	  gsub(/name = /,"",$0);				# call by reference
    tier=gensub(/\"/,"","g",$0);	# call by value
	}
  if ($0 ~ /intervals/) {
	  gsub(/intervals /,"",$0);
	  gsub(/\]/,"",$0);
	  gsub(/\[/,"",$0);
	  gsub(/:/,"",$0);
		interval=$0;
	}
  if ($0 ~ /xmin/) {
	  gsub(/xmin = /,"",$0);
	  gsub(/\./,",",$0);
		xmin=$0;
	}
  if ($0 ~ /xmax/) {
	  gsub(/xmax = /,"",$0);
	  gsub(/\./,",",$0);
	  xmax=$0;
	}
  if ($0 ~ /text = /) {
	  gsub(/text = /,"",$0);
	  gsub(/## /,"",$0);
		kontext=$0;
		n=split($0,arr," ");
		if (tier ~ /zodziai/) {
			for (i=1;i<=n;i++) {
				word = arr[i];
				#remove \"
				word = gensub(/^\"(.*)\"$/,"\\1","g",word);
				#remove stess information
				fixedword = word
				fixedword = gensub(/i:/,"y","g",fixedword);
				fixedword = gensub(/tS/,"Č","g",fixedword);
				fixedword = gensub(/Z/,"Ž","g",fixedword);
				fixedword = gensub(/E\:/,"Ė","g",fixedword);
				fixedword = gensub(/S/,"Š","g",fixedword);
				fixedword = gensub(/u\:/,"Ū","g",fixedword);
				fixedword = gensub(/a\:/,"Ą","g",fixedword);
				fixedword = gensub(/[\"'^\.:]/,"","g",fixedword);
				fixedword = toupper(fixedword);
				#if it is not silent
				if (word ~ /^\.\.\.$/) {
					#printf  ( "%s ", "<sil>");
					#print "<sil>","\t","<sil>"> "target/_lt_all-words.txt"
				}else{
					printf  ( "%s ", fixedword);
					print fixedword,"\t",word>> "target/_lt_all-words.txt"
				}
#				print  gensub(/ */,"","g",++j), gensub(/ */,"","g",tier), gensub(/ */,"","g",interval), gensub(/ */,"","g",i), gensub(/ */,"","g",xmin), gensub(/ */,"","g",xmax), gensub(/^ */,"","g",kontext), gensub(/[\",\.\{\}]/,"","g",arr[i]);
			}
		}
	}
}
END {
	printf( "</s>\n");
	#printf( "</s> (%s)\n", gensub(/^.*\/(.*).Textgrid$/,"\\1","g",FILENAME));
	print gensub(/.*wav\/(.*).Textgrid$/,"\\1","g",FILENAME)>> "target/_lt_all.fileids"
}


