#!/usr/bin/env python

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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
    f = sys.argv[2]
    xml_data = open(f).read()
    df = xml2df(xml_data)
    df.rename(columns={'ENAME':'State'},inplace=True)
    print(df)
    return df




def main():
    # Load the data
    f = sys.argv[1]
    data = pd.read_csv(f)
    
    data = data[data.Year >= 2019]
    datas = data[data.Period == 'YEAR']
    states = datas.State.unique()


    data = data[['State','Year','Value']]

    data['Value'] = data['Value'].str.replace(',','').astype(float)
    ha  = data.groupby(['State','Year']).mean().reset_index()
    print(ha)    
    ha['Value'] = ha.Value * 0.404686
    print(ha)
    tbl = read_ustbl()
    tbl = tbl[tbl['AREA1'] != 'AK']
    tbl = tbl[tbl['AREA1'] != 'HI']

    ha = ha.merge(tbl)[['Year','State','Value']]
    #ton_ha = ton_ha.set_index('Year')

    # ピボットテーブルを作成して、目的の形式に変換
    pivot_df = ha.pivot(index='State', columns='Year', values='Value')

    # 列の順序を変更（年順にソート）

    pivot_df = pivot_df.reindex(columns=sorted(pivot_df.columns))


    pivot_df.to_csv('field_output.csv', index=True)

    
if __name__ == '__main__':
    main()


    
