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
        outfile = outdir+"/"+state+"_WX_lrf.csv"
        df = pd.read_csv(outfile)
        print(df)
        dfs.append(df)
    df = pd.concat(dfs)
    #State,AREA1,date,TAVG_x,TAVG_NORYR,TMAX,TMAX_NORYR,TMIN,TMIN_NORYR,PRCP_x,PRCP_NORYR,WEEK_NO,DATE,MAX,MIN,PRCP_y,TAVG_y
    df = df.groupby(['date']).mean(numeric_only=True).reset_index()
    print(df)

    df['State'] = "Average"
    df['Area'] = "AVG"
    df['DATE'] = df['date']
    df = df[['State','Area','date','TAVG_x',
             'TAVG_NORYR','TMAX','TMAX_NORYR',
             'TMIN','TMIN_NORYR','PRCP_x','PRCP_NORYR','WEEK_NO','DATE','MAX','MIN',
             'PRCP_y','TAVG_y']]

    state = 'average'
    outdir = "/usr/amoeba/pub/crop/data"
    outfile = outdir+"/"+state+"_WX_lrf.csv"
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
        tavgs = []
        tavgs_norm = []
        tmaxs = []
        tmaxs_norm = []
        tmins = []
        tmins_norm = []        
        prcps = []
        prcps_norm = []
        
        point_data_ref = point_data_ary_ref[i]        
        state = point_data_ref["AREA"]
        area1 = point_data_ref["AREA1"]
        FCAS_count = point_data_ref["FCAS_count"]
        fcas_data_ary_ref = point_data_ref["FCAS_data"]
        
        for c in range(FCAS_count):
            fcas_data_ref = fcas_data_ary_ref[c]
            dates.append(fcas_data_ref["FCAS_date"].get_time().strftime("%Y%m%d"))
            tmaxs.append(fcas_data_ref['AIRTMP_MAX'])
            tmins.append(fcas_data_ref['AIRTMP_MIN'])
            tavgs.append(fcas_data_ref['AIRTMP_AVG'])
            prcps.append(fcas_data_ref['PRCRIN'] )
            tmaxs_norm.append(fcas_data_ref['AIRTMP_MAX_NORYR'])
            tmins_norm.append(fcas_data_ref['AIRTMP_MIN_NORYR'])
            prcps_norm.append(fcas_data_ref['PRCRIN_NORYR'] )
            tavgs_norm.append(fcas_data_ref['AIRTMP_AVG_NORYR'])
            """
            #                    FLOAT32	/area_data/17/FCAS_data/29/AIRTMP_AVG	-2.23333334922791
                    FLOAT32	/area_data/17/FCAS_data/29/AIRTMP_AVG_NORYR	-4.09999990463257
                    FLOAT32	/area_data/17/FCAS_data/29/AIRTMP_MAX	2.40000009536743
                    FLOAT32	/area_data/17/FCAS_data/29/AIRTMP_MAX_NORYR	0.5
                    FLOAT32	/area_data/17/FCAS_data/29/AIRTMP_MIN	-6.73333311080933
                    FLOAT32	/area_data/17/FCAS_data/29/AIRTMP_MIN_NORYR	-8.60000038146973
                    FLOAT32	/area_data/17/FCAS_data/29/PRCRIN	8.33333301544189
                    FLOAT32	/area_data/17/FCAS_data/29/PRCRIN_NORYR	9.46666622161865
            """
            #datetime,TMAX,TMIN,PRCP,State
        df = pd.DataFrame({"State":state,"AREA1":area1,"date":dates, "TAVG":tavgs,"TAVG_NORYR":tavgs_norm,"TMAX":tmaxs,"TMAX_NORYR":tmaxs_norm,"TMIN":tmins,"TMIN_NORYR":tmins_norm,"PRCP":prcps,"PRCP_NORYR":prcps_norm})
        
        #print(df)
        
        # Read 2024 obs data
        f = '/usr/amoeba/pub/crop/data/gosd/'+area1+'_2024_obs_weekly.csv'
        d = pd.read_csv(f)
        print(d)

        
        #df.index = pd.to_datetime(df['DATE'])
        d = d.rename(columns={'State':'AREA1'})
        d['DATE'] = pd.to_datetime(d['DATE'])
        df['date'] = pd.to_datetime(df['date'])
        df['WEEK_NO'] = df['date'].dt.isocalendar().week 
        print(df)
        d['WEEK_NO'] = d['DATE'].dt.isocalendar().week

        d = pd.merge(df,d,on=['WEEK_NO','AREA1'])
        print(d)

        #d = d.drop('WEEK_NO',axis=1)
        
        # output csv
        outdir = "/usr/amoeba/pub/crop/data"
        outfile = outdir+"/"+state+"_WX_lrf.csv"
        d.to_csv(outfile,index=False)
    
    

            

    
    return 0


f= sys.argv[1]
dump(f)
state_mean()
