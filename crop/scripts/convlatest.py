#!/usr/bin/env python

import pandas as pd
import sys



    
def main():
    arc_f = sys.argv[1]
    df2 = pd.read_csv('../data/field_output.csv')
    arc_f = pd.read_csv(arc_f)
    
    constant = 0.404686 * 0.021772 
    arc_f[arc_f.select_dtypes(include='number').columns] /= constant
    print(arc_f)

    #exit(0)
    #crop = df_f['2024'] * df2['2024']
    #arc_f[date] = crop


    # make latest.csv
    outdir = "/usr/amoeba/pub/crop/data"
    outfile = outdir + "/latest.csv"
    
    arc_f.to_csv(outfile,index=False)
    exit(0)
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
        

