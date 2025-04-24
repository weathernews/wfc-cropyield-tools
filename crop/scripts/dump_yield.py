#!/usr/bin/env python

import pandas as pd
import RU
import sys
import os
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
    f = "../tbl/USSTCC.xml"
    xml_data = open(f).read()
    df = xml2df(xml_data)
    df.rename(columns={'ENAME':'State'},inplace=True)

    return df


def dump(f):
    param = {}
    
    # Open file
    fp = open(f,"rb")
    #print(fp)

    # Read RU construct
    ru = RU.RU()
    root_ref = ru.load(fp)
    fp.close()

    header = ru.get_header()
    announced_date = root_ref["announced_date"].get_time().strftime("%Y-%m-%d")

    # get the number of points and the point array
    point_count = root_ref["area_count"]
    point_data_ary_ref = root_ref["area_data"]
    STATES = []
    AREAS = []
    YIELDS = []

    # print element values for each point
    for i in range(point_count):
        point_data_ref = point_data_ary_ref[i]
        STATES.append(point_data_ref["AREA"])
        AREAS.append(point_data_ref["AREA1"])
        YIELDS.append(point_data_ref["YIELD"])
    df = pd.DataFrame()
    df['State'] =  STATES
    df['AREA1'] =  AREAS
    df['YIELD'] = YIELDS
    df = df.replace(-99,np.nan)

    
    return df,announced_date


outdir = "/usr/amoeba/pub/crop/data"

f = sys.argv[1]
df,datetime = dump(f)
tbl = read_ustbl()
tbl = tbl[tbl['AREA1'] != 'AK']
tbl = tbl[tbl['AREA1'] != 'HI']


df = pd.merge(tbl,df,how="outer")
df['YIELD'] = df['YIELD'] / .021772

df['date'] = datetime

d = df.rename(columns={"YIELD":"Value"})

d.to_csv(outdir+"/ton_ha"+datetime[0:4]+'.csv')

df.set_index('State',inplace=True)

df.to_csv(outdir+"/"+datetime+'_yield.csv')
print(outdir+"/"+datetime+'_yield.csv')
