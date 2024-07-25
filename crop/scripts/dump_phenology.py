#!/usr/bin/env python

import pandas as pd
import RU
import sys
import os
import numpy as np

def dump(f):
    param = {}
    
    # Open file
    fp = open(f,"rb")
    print(fp)

    # Read RU construct
    ru = RU.RU()
    root_ref = ru.load(fp)
    fp.close()

    header = ru.get_header()
    announced_date = root_ref["announced_date"].get_time().strftime("%Y-%m-%d")

    # get the number of points and the point array
    point_count = root_ref["area_count"]
    point_data_ary_ref = root_ref["area_data"]
    STATES = []
    STAGE1 = []
    STAGE2 = []
    STAGE3 = []
    STAGE4 = []
    STAGE5 = []
    #["EMERGED",'BLOOMING','SETTING PODS','DROPPING LEAVS','HARVESTED']
    # print element values for each point
    for i in range(point_count):
        point_data_ref = point_data_ary_ref[i]
        STATES.append(point_data_ref["AREA"])
        STAGE1.append(point_data_ref["STAGE1"])
        STAGE2.append(point_data_ref["STAGE2"])
        STAGE3.append(point_data_ref["STAGE3"])
        STAGE4.append(point_data_ref["STAGE4"])
        STAGE5.append(point_data_ref["STAGE5"])
    df = pd.DataFrame()
    df['State'] =  STATES
    df['EMERGED'] =  STAGE1
    df['BLOOMING'] =  STAGE2
    df['SETTING PODS'] =  STAGE3
    df['DROPPING LEAVS'] = STAGE4
    df['HARVESTED'] = STAGE5
    #df['Date'] = announced_date
    df = df.replace(-99,np.nan)

    
    return df,announced_date


f= sys.argv[1]
df,datetime = dump(f)
print(df,datetime)
df['date'] = datetime
stages = ["EMERGED",'BLOOMING','SETTING PODS','DROPPING LEAVS','HARVESTED']
outdir = "/usr/amoeba/pub/crop/data" 
df.to_csv(outdir+'/'+"PROG_output.csv",index=False)

tbl2 = pd.read_csv('../tbl/state.tbl')
df = pd.merge(tbl2,df)
df.set_index('State',inplace=True)
df.to_csv(outdir+'/'+"PROG.csv")
for s in stages:
    d = df[[s]]
    d = d.rename({s:datetime},axis=1)
    # save dump file for index.html

    d.to_csv(outdir+'/'+s+"_prog.csv")
    #print(d)
