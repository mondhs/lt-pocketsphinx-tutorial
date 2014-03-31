#!/bin/bash
echo `date +"%T"`
START=$(date +%s);
sphinxtrain run
END=$(date +%s);
echo "Duration: $(($DIFF / 3600 )) hours $((($DIFF % 3600) / 60)) minutes $(($DIFF % 60)) seconds"

