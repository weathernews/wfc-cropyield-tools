#!/usr/bin/env python

import pandas as pd
import sys
import os


f1 = sys.argv[1]
f2 = "/usr/amoeba/pub/crop/data/yield_output.csv"# 2020-2024 収量

df1 = pd.read_csv(f1)
df1.date = pd.to_datetime(df1.date).dt.year
df1 = df1.rename(columns={"YIELD":df1.date.values[0]})
df1 = df1.drop(["AREA1","AREA"],axis=1)
df2 = pd.read_csv(f2)
print(df1.shape)
print(df2.shape)
df = pd.merge(df2,df1)
df = df.drop('date',axis=1)
df.to_csv("/usr/amoeba/pub/crop/data/YIELD_output.csv",index=False)

