#!/usr/bin/env python

import pandas as pd
import sys

f1 = sys.argv[1]
f2 = sys.argv[2]
f3 = sys.argv[3]


df1 = pd.read_csv(f1)
df2 = pd.read_csv(f2)
df3 = pd.read_csv(f3)
print(df1)
print(df2)

df1['Value'] = (df1['2024'] * df2['2024']) / 1000

df = pd.merge(df1,df3)
df = df.sort_values('Value',ascending=False)
df.set_index('State',inplace=True)
df = df.iloc[:,-6:-1]
df.to_csv(f3)
