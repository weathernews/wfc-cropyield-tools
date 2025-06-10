#!/usr/bin/env python

import pandas as pd
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
import os


def state_mean(area_df):



    pre_df = area_df[area_df['Year'] == 2024]
    now_df = area_df[area_df['Year'] == 2025]

    pre_df = pre_df.rename(columns={'TMAX':'2024 TMAX','TMIN':'2024 TMIN','PRCP':'2024 PRCP','TAVG':'2024 TAVG'})
    now_df = now_df.rename(columns={'TMAX':'2025 TMAX','TMIN':'2025 TMIN','PRCP':'2025 PRCP','TAVG':'2025 TAVG'})

    
    # 5年平均
    avg_df = area_df[area_df.Year <= 2024]
    avg_df = avg_df[avg_df.Year >= 2020]
    
    # 5年ごとのグループ列を追加
    avg_df['YearGroup'] = (avg_df['Year'] // 5) * 5

    # 平均を取る対象の列
    avg_cols = ['TAVG', 'TMIN', 'TMAX', 'PRCP']
    
    # 月ごと × 年グループ × エリア で集計（5年平均）
    avg_df= (
        avg_df.groupby(['YearGroup', 'Month','AREA_x'])[avg_cols]
        .mean()
        .reset_index()
    )
    
    avg_df = avg_df.rename(columns={'TMAX':'5AVG TMAX','TMIN':'5AVG TMIN','PRCP':'5AVG PRCP','TAVG':'5AVG TAVG'})


    df = pd.merge(pre_df,now_df,on='Month')[['Month','2024 TMAX','2025 TMAX','2024 TMIN','2025 TMIN','2024 PRCP','2025 PRCP','2024 TAVG','2025 TAVG']]

    
    df = pd.merge(df,avg_df,on='Month')[['Month','2024 TMAX','2025 TMAX','5AVG TMAX','2024 TMIN','2025 TMIN','5AVG TMIN','2024 PRCP','2025 PRCP','5AVG PRCP','2024 TAVG','2025 TAVG','5AVG TAVG']]
    return df

    
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


df1 = pd.read_csv(f1)


tbl = read_ustbl()
tbl = tbl[tbl['AREA1'] != 'AK']
tbl = tbl[tbl['AREA1'] != 'HI']
df1['DATE'] = pd.to_datetime(df1.DATE)




df1['Year'] = df1.DATE.dt.year

df1['Month'] = df1.DATE.dt.month



df1 = df1[['DATE','AREA','TAVG','TMIN','TMAX','PRCP','Year','Month']]

df = df1  # まず df1 をデフォルトとして代入
# 現在時刻を取得
now = datetime.now()
if now.month == 1 :
    prev_month_start = datetime(now.year - 1, 11, 1)
elif now.month == 2:
    prev_month_start = datetime(now.year - 1, 12, 1)
else:
    prev_month_start = datetime(now.year, now.month - 2, 1)

prev_month_str = prev_month_start.strftime('%Y-%m-%d')
if len(sys.argv) > 2:
    f2 = sys.argv[2]
    if os.path.exists(f2):
        df2 = pd.read_csv(f2)
        df2['DATE'] = pd.to_datetime(df2.DATE)
        df2.set_index('DATE', inplace=True)
        df2 = df2[prev_month_str:"2025-12-31"].reset_index()
        df2['Year'] = df2.DATE.dt.year
        df2['Month'] = df2.DATE.dt.month
        df2 = df2.rename(columns={'State': 'AREA', 'MIN': 'TMIN', 'MAX': 'TMAX'})
        
        df = pd.concat([df1, df2])


tbl = tbl[tbl['AREA1'] != 'AK']
tbl = tbl[tbl['AREA1'] != 'HI']
wx = df
# 現在の月を取得
current_month = datetime.now().month

#月から先月までのリストを作成
months_list = list(range(1, current_month ))
f_df = wx[wx['Month'].isin(months_list)]
f_df.reset_index(inplace=True)
f_df = pd.merge(f_df,tbl,left_on='AREA',right_on='AREA1')
print(f_df)
states = ['ILLINOIS','IOWA','MINNESOTA','INDIANA','OHIO','MISSOURI','NEBRASKA','NORTH DAKOTA','SOUTH DAKOTA','ARKANSAS','KANSAS','MISSISSIPPI','WISCONSIN','KENTUCKY','MICHIGAN','TENNESSEE','NORTH CAROLINA','LOUISIANA']
f_df =  f_df[f_df['State'].isin(states)]
print(f_df)
## 対象期間に絞る


#f_df = f_df[(f_df['Year'] >= 2020) & (f_df['Year'] <= 2024)]
for state in f_df['State'].unique():
    area_df = f_df[f_df['State'] == state]    
    df = state_mean(area_df)
    
    df.to_csv('../data/'+state+'_WX_output.csv',index=False)




# 全州の平均値を作る
df_2020_2024 = f_df[(f_df['Year'] >= 2020) & (f_df['Year'] <= 2024)]
# === Step 2: 2024年と2025年だけ別で抜き出す ===
df_2024 = f_df[f_df['Year'] == 2024]
df_2025 = f_df[f_df['Year'] == 2025]

# === Step 3: 月ごとの全国平均をそれぞれ計算 ===
avg_cols = ['TAVG', 'TMIN', 'TMAX', 'PRCP']

monthly_2024 = df_2024.groupby('Month')[avg_cols].mean().reset_index()
monthly_2025 = df_2025.groupby('Month')[avg_cols].mean().reset_index()
monthly_5yr  = df_2020_2024.groupby('Month')[avg_cols].mean().reset_index()

# === Step 4: カラム名をリネーム（分かりやすく） ===
monthly_2024 = monthly_2024.rename(columns={
    'TAVG': '2024 TAVG', 'TMIN': '2024 TMIN', 'TMAX': '2024 TMAX', 'PRCP': '2024 PRCP'
})

monthly_2025 = monthly_2025.rename(columns={
    'TAVG': '2025 TAVG', 'TMIN': '2025 TMIN', 'TMAX': '2025 TMAX', 'PRCP': '2025 PRCP'
})

monthly_5yr = monthly_5yr.rename(columns={
    'TAVG': '5AVG TAVG', 'TMIN': '5AVG TMIN', 'TMAX': '5AVG TMAX', 'PRCP': '5AVG PRCP'
})

# === Step 5: 月をキーに順にマージ ===
df_merge = pd.merge(monthly_2024, monthly_2025, on='Month')
df_merge = pd.merge(df_merge, monthly_5yr, on='Month')[['Month','2024 TMAX','2025 TMAX','5AVG TMAX','2024 TMIN','2025 TMIN','5AVG TMIN','2024 PRCP','2025 PRCP','5AVG PRCP','2024 TAVG','2025 TAVG','5AVG TAVG']]
#df = pd.merge(df,avg_df,on='Month')
# === Step 6: 出力 ===
print(df_merge)
df_merge.to_csv('../data/average_WX_output.csv',index=False)
