#!/bin/bash

SCRIPT_DIR=$(cd $(dirname $0); pwd)
cd $SCRIPT_DIR

# update obs data
aws s3 cp --no-sign-request s3://noaa-gsod-pds/2025/ ../data/gsod/. --exclude "*" --include "72*.csv" --recursive 

# 解析
python3.7 read_gsod.py

python3.7 merge_gsod_gsom.py ../data/WX_output.csv ../data/gsod/2025_obs_monthly.csv 


exit
