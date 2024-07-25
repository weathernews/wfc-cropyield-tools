#!/usr/bin/env python

import pandas as pd
import sys



    
def main():
    f = sys.argv[1]
    arc_f = sys.argv[2]
    date = sys.argv[3]
    
    df2 = pd.read_csv('../data/field_output.csv')
    df_f = pd.read_csv(f)
    
    arc_f = pd.read_csv(arc_f)
    
    crop = df_f['2024'] * df2['2024']
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

    # 結果を表示
    print(df_melted[['State', 'datetime', 'value']])
    
    for state in df_melted['State'].unique():
        df = df_melted[df_melted.State == state]
        df['datetime'] = pd.to_datetime(df['datetime'],format="%Y-%m-%d")

        df = df.sort_values(by='datetime')
        df = df[1:]
        print(df)

        
        df.to_csv('../data/'+state+'_latest.csv',index=False)
        

