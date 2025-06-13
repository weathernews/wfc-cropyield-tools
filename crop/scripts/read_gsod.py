#!/usr/bin/env python3

import pandas as pd
import numpy as np
import sys
import glob
def read_gsod():
    files = glob.glob('../data/gsod/72*.csv')
    df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
    
    return df

def main():
    df = read_gsod()

    df = df[['NAME','DATE','MAX','MIN','PRCP']]
    df = df.dropna()
    
    df = df[df.MAX != 9999.9]
    df = df[df.MIN != 9999.9]
    df = df[df.PRCP != 99.99]
    df.MAX = (df.MAX - 32) * 5/9
    df.MIN = (df.MIN - 32) * 5/9
    df.PRCP = df.PRCP * 25.4

    # 州を抽出（例： "Phoenix, AZ US" → "AZ"）
    df['State'] = df.NAME.str.extract(r',\s*([A-Z]{2})\s')
    # 日付を datetime に変換（必要に応じて）
    df['DATE'] = pd.to_datetime(df['DATE'])
    print(df.State.unique())
    # 数値列だけ抽出
    numeric_cols = df.select_dtypes(include='number').columns



    df = df.groupby(['State', 'DATE'])[numeric_cols].mean().reset_index()

    df = df.dropna()
    df.DATE = pd.to_datetime(df.DATE)
    df.set_index('DATE', inplace=True)

    dfs = []

    
    for state in df.State.unique():
        df1 = df[df.State == state]
        df1['TAVG'] = (df1['MAX'] + df1['MIN']) / 2
        print(df1)

        df2 = df1.select_dtypes(include='number').resample('M').mean().reset_index()
        PRCP = df1.select_dtypes(include='number').resample('M').sum().reset_index()['PRCP']
        #df2 = df1.resample('M').mean(numeric_only=True).reset_index()

        #PRCP = df1.resample('M').sum(numeric_only=True).reset_index()['PRCP']
        df2['State'] = state
        df2['PRCP'] = PRCP

        print(df2.MAX.max())
        print(df2.MIN.max())
        print(df2.PRCP.max())
        dfs.append(df2)
    df = pd.concat(dfs)
    print(df)
    df.to_csv(f'../data/gsod/2025_obs_monthly.csv', index=False)

if __name__ == '__main__':
    main()
