#!/bin/bash

## DUMP & Create csv for index.html
# Config
SCRIPT_DIR=$(cd $(dirname $0); pwd)
cd $SCRIPT_DIR
OUTDIR="/usr/amoeba/pub/crop/data" 
RUFILE=${1}

# Dump
echo python3.7 dump_yield.py $RUFILE
outfile=`python3.7 dump_yield.py $RUFILE`
echo $outfile

# Merge 2019-2023 & latest YIELD
python3.7 merge_yield.py $outfile

# Make latest csv
date=`basename $outfile _yield.csv`

python3.7 add_latest.py $OUTDIR/YIELD_output.csv $OUTDIR/latest.csv $date
echo python3.7 add_latest.py $OUTDIR/YIELD_output.csv $OUTDIR/latest.csv $date

# Plot Png
python3.7 plot_yield.py $date

echo "Done. dump csv"
exit
