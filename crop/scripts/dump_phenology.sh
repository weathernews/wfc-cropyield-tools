#!/bin/bash

## DUMP & Create csv for index.html
# Config
SCRIPT_DIR=$(cd $(dirname $0); pwd)
cd $SCRIPT_DIR
OUTDIR="/usr/amoeba/pub/crop/data" 
RUFILE=${1}

# Dump
echo python3.7 dump_phenology.py $RUFILE
python3.7 dump_phenology.py $RUFILE

# Merge & sort

YIELD_FILE=$OUTDIR/"YIELD_output.csv"
FIELD_FILE=$OUTDIR/"field_output.csv"
f="$OUTDIR/PROG.csv"
python3.7 merge.py "$YIELD_FILE" "$FIELD_FILE" "$f"



# Plot Png
python3.7 plot_phenology.py

exit


