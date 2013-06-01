#awk -f test.awk wav/ak1/AK1/fva.Textgrid
BEGIN {
  OFS = "\t";
  print "Datei\tid\t\"Tier\"\tInterval\tposition\txmin\txmax\tkontext\twort" >"tabelle_wort.txt";
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
		for (i=1;i<=n;i++) {
  	  print FILENAME, gensub(/ */,"","g",++j), gensub(/ */,"","g",tier), gensub(/ */,"","g",interval), gensub(/ */,"","g",i), gensub(/ */,"","g",xmin), gensub(/ */,"","g",xmax), gensub(/^ */,"","g",kontext), gensub(/[\",\.\{\}]/,"","g",arr[i]) >>"tabelle_wort.txt";
		}
	}
}

