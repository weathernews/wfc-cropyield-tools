#!/usr/bin/env python

import pandas as pd
import sys
import xml.etree.ElementTree as ET
from datetime import datetime

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
    f = '../tbl/USSTCC.xml'
    xml_data = open(f).read()
    df = xml2df(xml_data)
    df.rename(columns={'ENAME':'State'},inplace=True)
    print(df)
    return df

f1 = sys.argv[1]
f2 = sys.argv[2]

df1 = pd.read_csv(f1)
df2 = pd.read_csv(f2)
print(df1)
print(df2)

tbl = read_ustbl()
tbl = tbl[tbl['AREA1'] != 'AK']
tbl = tbl[tbl['AREA1'] != 'HI']
df1['DATE'] = pd.to_datetime(df1.DATE)
df2['DATE'] = pd.to_datetime(df2.DATE)
df2.set_index('DATE',inplace=True)
df2 = df2["2024-05-31":"2024-12-31"]
df2 = df2.reset_index()
print(df2)


df1['Year'] = df1.DATE.dt.year
df2['Year'] = df2.DATE.dt.year
df1['Month'] = df1.DATE.dt.month
df2['Month'] = df2.DATE.dt.month
df2 = df2.rename(columns={'State':'AREA','MIN':'TMIN','MAX':'TMAX'})

df1 = df1[['DATE','AREA','TAVG','TMIN','TMAX','PRCP','Year','Month']]
print(df1)
print(df2)
df = pd.concat([df1,df2])
print(df)

tbl = tbl[tbl['AREA1'] != 'AK']
tbl = tbl[tbl['AREA1'] != 'HI']
wx = df
# 現在の月を取得
current_month = datetime.now().month

# 1月から先月までのリストを作成
months_list = list(range(1, current_month ))
f_df = wx[wx['Month'].isin(months_list)]
f_df.reset_index(inplace=True)
f_df = pd.merge(f_df,tbl,left_on='AREA',right_on='AREA1')
print(f_df)

for state in f_df['State'].unique():
    area_df = f_df[f_df['State'] == state]    
    temperature_df = area_df[['TMAX', 'TMIN','PRCP','TAVG','Month','Year']]
    
    #df = temperature_df.mean()
    #print(df)

    temperature_df.index = temperature_df['Month']  # 日付をインデックスとして設定
    print(temperature_df,temperature_df.Year)
    #exit(0)
    
    pre_df = area_df[area_df.Year == 2023]
    now_df = area_df[area_df.Year == 2024]
    pre_df = pre_df.rename(columns={'TMAX':'2023 TMAX','TMIN':'2023 TMIN','PRCP':'2023 PRCP','TAVG':'2023 TAVG'})
    now_df = now_df.rename(columns={'TMAX':'2024 TMAX','TMIN':'2024 TMIN','PRCP':'2024 PRCP','TAVG':'2024 TAVG'})
    df = pd.merge(pre_df,now_df,on='Month')[['Month','2023 TMAX','2024 TMAX','2023 TMIN','2024 TMIN','2023 PRCP','2024 PRCP','2023 TAVG','2024 TAVG']]
    print(df)

    df.to_csv('../data/'+state+'_WX_output.csv',index=False)


#df.to_csv('merge.csv',index=False)
#df1 = df1.rename(columns={'AREA':'State','PRCP':'PRCP_1'})
#print(df1)



#print(df)


