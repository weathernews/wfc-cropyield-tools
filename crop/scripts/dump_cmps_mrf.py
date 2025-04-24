#!/usr/bin/python3.7

import pandas as pd
import RU
import sys
import os
import numpy as np
def state_mean():
    states = ['ILLINOIS','IOWA','MINNESOTA','INDIANA','OHIO','MISSOURI','NEBRASKA','NORTH DAKOTA','SOUTH DAKOTA','ARKANSAS','KANSAS','MISSISSIPPI','WISCONSIN','KENTUCKY','MICHIGAN','TENNESSEE','NORTH CAROLINA','LOUISIANA']
    outdir = "/usr/amoeba/pub/crop/data"
    dfs = []
    for state in states:
        state = state.replace(" ","")
        outfile = outdir+"/"+state+"_WX_mrf.csv"
        df = pd.read_csv(outfile)

        dfs.append(df)
    df = pd.concat(dfs)

    #dateitme       TMAX       TMIN       PRCP
    df = df.groupby(['datetime']).mean(numeric_only=True).reset_index()
    print(df)
    state = 'average'
    outdir = "/usr/amoeba/pub/crop/data"
    outfile = outdir+"/"+state+"_WX_mrf.csv"
    df.to_csv(outfile,index=False)
    
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
    # print element values for each point
    for i in range(point_count):
        dfs = []
        dates = []
        tmaxs = []
        tmins = []
        prcps = []
        
        point_data_ref = point_data_ary_ref[i]        
        state = point_data_ref["AREA"]
        FCAS_count = point_data_ref["FCAS_count"]
        fcas_data_ary_ref = point_data_ref["FCAS_data"]
        
        for c in range(FCAS_count):
            fcas_data_ref = fcas_data_ary_ref[c]
            dates.append(fcas_data_ref["FCAS_date"].get_time().strftime("%Y%m%d"))
            tmaxs.append(fcas_data_ref['AIRTMP_MAX'])
            tmins.append(fcas_data_ref['AIRTMP_MIN'])
            prcps.append(fcas_data_ref['PRCRIN'] )
        #datetime,TMAX,TMIN,PRCP,State
        df = pd.DataFrame({"datetime":dates, "TMAX":tmaxs,"TMIN":tmins,"PRCP":prcps})


        
        # output csv
        outdir = "/usr/amoeba/pub/crop/data"
        outfile = outdir+"/"+state+"_WX_mrf.csv"
        df.to_csv(outfile,index=False)
        print("UPDATE:"+outfile)
    
    return 0

if __name__ == "__main__":
    f = sys.argv[1]
    dump(f)
    state_mean()
