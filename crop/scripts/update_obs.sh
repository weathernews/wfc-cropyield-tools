#!/bin/bash

SCRIPT_DIR=$(cd $(dirname $0); pwd)
cd $SCRIPT_DIR

# update obs data
outdata="../data/gsod/2024.tar.gz"
wget https://www.ncei.noaa.gov/data/global-summary-of-the-day/archive/2024.tar.gz -O $outdata

# 解凍
tar -zxvf $outdata -C "../data/gsod/"

# 解析
python3.7 read_gsod.py

python3.7 merge_gsod_gsom.py ../data/WX_output.csv ../data/gsod/2024_obs_monthly.csv 


exit
