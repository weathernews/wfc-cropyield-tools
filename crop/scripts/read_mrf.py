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
            df['TMAX'] = values['AIRTMP_MAX']
            df['TMIN'] = values['AIRTMP_MINI']
            df['PRCP'] = values['PRCRIN']
            dfs.append(df)
            
df = pd.concat(dfs)
df = df.merge(df_tbl)
df = df.replace(-9999.0, np.nan)
df = df.dropna()
df.to_csv('test.csv')
#print(df)


gdf  = df.groupby(['AREA1','date']).mean().reset_index()

tbl = read_ustbl()
tbl = tbl[tbl['AREA1'] != 'AK']
tbl = tbl[tbl['AREA1'] != 'HI']
gdf = gdf.merge(tbl)
gdf
#for state in gdf.State.unique():
#    df = gdf[gdf.State == state]
#    df.to_csv(state+'_WX_lrf.csv',index=False)
    




    
    

