#!/usr/bin/env python

import pandas as pd
import sys
import os


    
def main():
    f = sys.argv[1]
    arc_f_path = sys.argv[2]
    date = sys.argv[3]
    
    df2 = pd.read_csv('../data/field_output.csv')
    df_f = pd.read_csv(f)

    if os.path.exists(arc_f_path):
        arc_f = pd.read_csv(arc_f_path)
    else:
        print(f"[INFO] {arc_f_path} が見つかりません。新しいDataFrameを作成します。")
        arc_f = pd.DataFrame()
        arc_f.index.name = 'no'
        arc_f.reset_index(inplace=True)

    merged = df_f.merge(df2, on=['State'])
    print(merged)

    crop = merged['2025_x'] * merged['2025_y']
    arc_f['State'] = merged['State']
    arc_f[date] = crop


    # make latest.csv
    outdir = "/usr/amoeba/pub/crop/data"
    outfile = outdir + "/latest.csv"
    
    arc_f.to_csv(outfile,index=False)
    
    return arc_f

if __name__ == "__main__":
    df = main()
    df = df.drop('no',axis=1)
    # データフレームを "長い形式"に変換
    df_melted = df.melt(id_vars=['State'], var_name='datetime', value_name='value')

    # 全州の月別平均と合計を計算
    df_avg = (
        df_melted
        .groupby('datetime', as_index=False)['value']
        .mean()

    )
    df_avg['State'] = 'Average'
    df_avg = df_avg[['State','datetime','value']]

    df_sum = (
        df_melted
        .groupby('datetime', as_index=False)['value']
        .sum()

    )
    df_sum['State'] = 'Average'
    df_sum = df_sum[['State','datetime','value']]
    
    
    # 保存
    df_avg.to_csv("../data/average_latest.csv", index=False)
    df_sum.to_csv("../data/sum_latest.csv", index=False)
    

    
    # 結果を表示
    print(df_melted[['State', 'datetime', 'value']])

    for state in df_melted['State'].unique():
        
        df = df_melted[df_melted.State == state]
        print(df)
        df['datetime'] = pd.to_datetime(df['datetime'],format="%Y-%m-%d")
        
        df = df.sort_values(by='datetime')
        #df = df[1:]
        print(df)

        
        df.to_csv('../data/'+state+'_latest.csv',index=False)
        

