#!/usr/bin/env python

import pandas as pd
import geopandas as gpd
import sys
import json
import numpy as np
import xml.etree.ElementTree as ET

def xml2df(xml_data):
    root = ET.XML(xml_data) # element tree
    all_records = []
    for i, child in enumerate(root):
        record = {}
        for subchild in child:
            record[subchild.tag] = subchild.text
        all_records.append(record)
    df = pd.DataFrame(all_records)
    return df


def read_ustbl():
    f = './USSTCC.xml'
    xml_data = open(f).read()
    df = xml2df(xml_data)
    df.rename(columns={'ENAME':'State'},inplace=True)
    print(df)
    return df


def readtbl(f):
    dfs = []

    with open(f, encoding='utf-8') as f:
        d = json.load(f)
        #for k in d.keys():
        #    print(k)
        for v in (d['features']):
            C = v['properties']['COUNTRY']
            if C == 'UNITED STATES':
                df = pd.DataFrame()
                ids = v['properties']['LOCAL_POINT_CD']
                name = v['properties']['POINT_NAME']
                names = name.split(' ')
                
                area = names[-1].split('.')[0]

                print(ids,name,area)
                df['ids'] = [ids]
                #df['NAME'] = [name]
                df['AREA1'] = [area]
                dfs.append(df)

    df = pd.concat(dfs)
    return df



f = sys.argv[1]
tbl = sys.argv[2]

df_tbl = readtbl(tbl)

rowsroot = "p_fcas_data"
# JSONファイルを読込
with open(f, encoding='utf-8') as f:
    d = json.load(f)


# Basetime , 地点数取得
basetime = d['basetime']
num = d['p_count']

# p_fcas_data だけ取得
if rowsroot != '':
    d = d[rowsroot]

dfs = []
for k,v in d.items():
    ids = k
    if k in df_tbl['ids'].values:
        print(k)
        for values in v:
            
            df = pd.DataFrame()
            df['ids'] = [k]
            df['date'] = values['FCASD']
            df['TAVG'] = values['AIRTMP_AVG']
            df['TAVG_NORYR'] = values['AIRTMP_AVG_NORYR']
            df['TMAX'] = values['AIRTMP_MAX']
            df['TMAX_NORYR'] = values['AIRTMP_MAX_NORYR']
            df['TMIN'] = values['AIRTMP_MINI']
            df['TMIN_NORYR'] = values['AIRTMP_MINI_NORYR']
            df['PRCP'] = values['PRCRIN']
            df['PRCP_NORYR'] = values['PRCRIN_NORYR']
            dfs.append(df)
            
df = pd.concat(dfs)
print(df)

#print(df_tbl)
df = df.merge(df_tbl)


#print(df)


#exit(0)
df = df.replace(-9999.0, np.nan)
df = df.dropna()
#df.to_csv('test.csv')

tbl = read_ustbl()
print(tbl)
#exit(0)
tbl = tbl[tbl['AREA1'] != 'AK']
tbl = tbl[tbl['AREA1'] != 'HI']

gdf = df.merge(tbl)
print(gdf)
#print(gdf)
#print(tbl)
#gdf = df.merge(tbl)
#



gdf = gdf.drop('ids',axis=1)
gdf  = gdf.groupby(['AREA1','date','State']).mean(numeric_only=True).reset_index()

#tbl = read_ustbl()
#tbl = tbl[tbl['AREA1'] != 'AK']
#tbl = tbl[tbl['AREA1'] != 'HI']
#gdf = gdf.merge(tbl)



for state in gdf.State.unique():
    d = gdf[gdf.State == state]
    AREA1 = d['AREA1'].unique()[0]
    print(AREA1)
    f = '../data/gosd/'+AREA1+'_2023_obs_weekly.csv'
    df = pd.read_csv(f)
    #df.index = pd.to_datetime(df['DATE'])
    df['DATE'] = pd.to_datetime(df['DATE'])
    d['date'] = pd.to_datetime(d['date'])
    df['WEEK_NO'] = df['DATE'].dt.isocalendar().week +1
    d['WEEK_NO'] = d['date'].dt.isocalendar().week
    print(df)
    print(d)
    d = pd.merge(d,df,on='WEEK_NO')
    print(d)

    #d = d.drop('ids',axis=1)
    #print(state)
    #d = d.groupby(['AREA1','date']).mean().reset_index()
    d.to_csv('../data/'+state+'_WX_lrf.csv',index=False)
    




    
    

