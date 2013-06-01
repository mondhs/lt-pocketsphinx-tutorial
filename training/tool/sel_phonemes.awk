/            xmin = / {begin = $3}
/            xmax = / {end = $3}
/            text = "/ {
        printf "%20s %10s %6.3f %6.3f\n", FILENAME, $3, begin, end
        }
