#!/usr/bin/python3.7

import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
from matplotlib.ticker import FuncFormatter
import matplotlib.colors as mcolors
import os,sys
import math
import cgi
from io import BytesIO
#import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import warnings
from shapely.errors import ShapelyDeprecationWarning
import matplotlib.style as mplstyle
mplstyle.use('fast')

# ShapelyDeprecationWarning を無視する
warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)



def output_rgba_array_to_stdout(rgba_array):
    # NumPy 配列から PIL Image オブジェクトを作成
    img = Image.fromarray(rgba_array, 'RGBA')
    
    # メモリ上のバイトストリームを作成
    byte_stream = BytesIO()
    
    # 画像をバイトストリームに保存
    img.save(byte_stream, 'PNG')
    
    # バイトストリームを取得
    image_data = byte_stream.getvalue()
    
    # 標準出力にバイナリとして書き出す
    sys.stdout.buffer.write(image_data)

    return 0
# Apply this to the gdf to ensure all states are assigned colors by the same func
def makeColorColumn(gdf,variable,vmin,vmax,colormap):
    # apply a function to a column to create a new column of assigned colors & return full frame
    norm = mcolors.Normalize(vmin=vmin, vmax=vmax, clip=True)
    cmap = plt.cm.get_cmap(colormap)
    cmap.set_bad(color='gray')
    mapper = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    gdf['value_determined_color'] = gdf[variable].apply(lambda x: mcolors.to_hex(mapper.to_rgba(x)))


    #gdf[gdf.value_determined_color.isna()] = '#ffffff'
    return gdf


def plot_prog(stage):

    f = "/usr/amoeba/pub/crop/data/PROG_output.csv"
    df = pd.read_csv(f)
    df = df.replace(0,np.nan)
    df = df.replace(-99,np.nan)
    date = df['date'].values[0]

    #df = df[['AREA1','Value']]
    
    gdf = gpd.read_file(os.getcwd()+'/../cb_2018_us_state_20m.shp')
    gdf = gdf[gdf.STUSPS != 'AK']
    gdf = gdf[gdf.STUSPS != 'HI']

    gdf['NAME'] = gdf.NAME.str.upper()
    gdf1 = gdf.merge(df,left_on='NAME',right_on='State')


    #printfg(gdf.STUSPS.unique())
    #gdf1 = gdf.merge(df,left_on='STUSPS',right_on='AREA1')


    tbl = pd.read_csv('../tbl/state.tbl')
    gdf1[stage] = gdf1.apply(lambda row: row[stage] if row['NAME'] in tbl['State'].values else np.nan,
                            axis=1
                            )





    # **************************
    # set the value column that will be visualised
    variable = stage
    
    # make a column for value_determined_color in gdf
    # set the range for the choropleth values with the upper bound the rounded up maximum value
    #vmin, vmax = gdf1.Value.min(), gdf1.Value.max() #math.ceil(gdf.pct_food_insecure.max())
    vmin = 0
    vmax = 99
    #Choose the continuous colorscale "YlOrBr" from https://matplotlib.org/stable/tutorials/colors/colormaps.html
    colormap = "YlGn"
    
    gdf1 = makeColorColumn(gdf1,variable,vmin,vmax,colormap)
    
    # create "visframe" as a re-projected gdf using EPSG 2163 for CONUS
    visframe = gdf1.to_crs({'init':'epsg:2163'})
    
    # create figure and axes for Matplotlib
    fig, ax = plt.subplots(1, figsize=(18, 14))
    # remove the axis box around the vis
    ax.axis('off')
    # set the font for the visualization to Helvetica
    title = 'Soybean Crop Progress:'+stage+' '+date
    ax.set_title(title, fontdict={'fontsize': '40', 'fontweight' : 'bold',})
    # Create colorbar legend
    fig = ax.get_figure()
    # add colorbar axes to the figure
    # This will take some iterating to get it where you want it [l,b,w,h] right
    # l:left, b:bottom, w:width, h:height; in normalized unit (0-1)
    cbax = fig.add_axes([0.93, 0.20, 0.03, 0.40])   

    title = 'Progrres:'+stage
    #cbax.set_title('Percentage of state households\nexperiencing food insecurity\n', **hfont, fontdict={'fontsize': '15', 'fontweight' : '0'})
    cbax.set_title(title,fontdict={'fontsize': '12', 'fontweight' : 'bold'})

    # add color scale
    sm = plt.cm.ScalarMappable(cmap=colormap, \
                               norm=plt.Normalize(vmin=vmin, vmax=vmax))
    # reformat tick labels on legend
    sm._A = []
    comma_fmt = FuncFormatter(lambda x, p: format(x/100, '.0%'))
    fig.colorbar(sm, cax=cbax, format=comma_fmt)
    #fig.colorbar(sm, cax=cbax)
    tick_font_size = 16
    cbax.tick_params(labelsize=tick_font_size)
    # annotate the data source, date of access, and hyperlink



    # create map

    # DataFrameを辞書形式に変換する
    visframe_dict = visframe.to_dict(orient='records')
    # 各行のデータに対して操作を行う
    for row in visframe_dict:
        vf = visframe[visframe['STUSPS'] == row['STUSPS']]    
        c = vf['value_determined_color'].item()
        # 一度にプロットする
        vf.plot(color=c, linewidth=0.8, ax=ax, edgecolor='0.8')
        
    # ADD LABELS
    visframe.apply(lambda x: ax.annotate(text=x.STUSPS, xy=x.geometry.centroid.coords[0], ha='center', fontsize=14,color='black',fontweight="bold"),axis=1);

    # グラフの周囲の余計な空白を除去                                                                                                                              
    fig.tight_layout()
    
    # 標準出力                                                                                                                                                    
    #fig.canvas.draw()
    #im = np.array(fig.canvas.renderer.buffer_rgba())
    ##fin = cv2.cvtColor(im, cv2.COLOR_RGBA2RGB)
    #sys.stdout.buffer.write(b'Content-type: image/png\n\n')
    #output_rgba_array_to_stdout(im)
    #plt.savefig(sys.stdout.buffer, format='png')
    plt.savefig('../png/'+stage+'_usa.png')
def plot_yeild():

    filename = './data/ton_ha'+str(year)+'.csv'
    filename2 = './data/field_ha'+str(year)+'.csv'
    # load the excel file into a pandas dataframe & skip header rows
    #df = pd.read_excel(filename,skiprows=4)
    df = pd.read_csv(filename)
    df2 = pd.read_csv(filename2)

    df['Value'] = df['Value'] * df2['Value'] / 1000
    

    df = df[['AREA1','Value']]
    
    gdf = gpd.read_file(os.getcwd()+'/cb_2018_us_state_20m.shp')
    gdf = gdf[gdf.STUSPS != 'AK']
    gdf = gdf[gdf.STUSPS != 'HI']
    
    #print(gdf.STUSPS.unique())
    #gdf1 = gdf.merge(df,left_on='STUSPS',right_on='AREA1')
    gdf1 = gdf.merge(df,left_on='STUSPS',right_on='AREA1')
    gdf1['NAME'] = gdf1.NAME.str.upper()
    tbl = pd.read_csv('./state.tbl')
    gdf1['Value'] = gdf1.apply(lambda row: row['Value'] if row['NAME'] in tbl['NAME'].values else np.nan,
                               axis=1
                               )




    # **************************
    # set the value column that will be visualised
    variable = 'Value'
    
    # make a column for value_determined_color in gdf
    # set the range for the choropleth values with the upper bound the rounded up maximum value
    #vmin, vmax = gdf1.Value.min(), gdf1.Value.max() #math.ceil(gdf.pct_food_insecure.max())
    vmin = 0 * 100
    #vmax = 4.4 * 1000
    #vmin = 1.5 * 1000
    vmax = 5.9 * 1000
    #Choose the continuous colorscale "YlOrBr" from https://matplotlib.org/stable/tutorials/colors/colormaps.html
    colormap = "YlOrBr"
    #gdf1 = gdf1.fillna(0)
    
    
    gdf1 = makeColorColumn(gdf1,variable,vmin,vmax,colormap)

    # create "visframe" as a re-projected gdf using EPSG 2163 for CONUS
    visframe = gdf1.to_crs({'init':'epsg:2163'})
    #visframe = gdf1
    
    
    # create figure and axes for Matplotlib
    fig, ax = plt.subplots(1, figsize=(18, 14))
    # remove the axis box around the vis
    ax.axis('off')
    
    # set the font for the visualization to Helvetica
    #title = 'Soybean Crop Yield (t/ha) '+str(year)
    title = 'Soybean Crop Yield (Metric ton) '+str(year)
    ax.set_title(title, fontdict={'fontsize': '42', 'fontweight' : 'bold',})
    # Create colorbar legend
    fig = ax.get_figure()
    # add colorbar axes to the figure
    # This will take some iterating to get it where you want it [l,b,w,h] right
    # l:left, b:bottom, w:width, h:height; in normalized unit (0-1)
    cbax = fig.add_axes([0.93, 0.20, 0.03, 0.30])   

    title = 'Crop Yield '
    #cbax.set_title('Percentage of state households\nexperiencing food insecurity\n', **hfont, fontdict={'fontsize': '15', 'fontweight' : '0'})
    cbax.set_title(title,fontdict={'fontsize': '15', 'fontweight' : '0','fontweight':'bold'})

    # add color scale
    sm = plt.cm.ScalarMappable(cmap=colormap, \
                               norm=plt.Normalize(vmin=vmin, vmax=vmax))
    # reformat tick labels on legend
    sm._A = []
    #comma_fmt = FuncFormatter(lambda x, p: format(x/100, '.0%'))
    #fig.colorbar(sm, cax=cbax, format=comma_fmt)
    fig.colorbar(sm, cax=cbax)
    tick_font_size = 16
    cbax.tick_params(labelsize=tick_font_size)
    # annotate the data source, date of access, and hyperlink



    # create map

    # DataFrameを辞書形式に変換する
    visframe_dict = visframe.to_dict(orient='records')
    # 各行のデータに対して操作を行う
    for row in visframe_dict:
        vf = visframe[visframe['STUSPS'] == row['STUSPS']]    
        #c = gdf1[gdf1['STUSPS'] == row['STUSPS']][0:1]['value_determined_color'].item()
        c = vf['value_determined_color'].item()
        # 一度にプロットする
        vf.plot(color=c, linewidth=0.8, ax=ax, edgecolor='0.8')
        
    # ADD LABELS
    visframe.apply(lambda x: ax.annotate(text=x.STUSPS, xy=x.geometry.centroid.coords[0], ha='center', fontsize=14,color='black',fontweight="bold"),axis=1);
    
    # グラフの周囲の余計な空白を除去                                                                                                                              
    fig.tight_layout()
    
    # 標準出力                                                                                                                                                    
    #fig.canvas.draw()
    #im = np.array(fig.canvas.renderer.buffer_rgba())
    #fin = cv2.cvtColor(im, cv2.COLOR_RGBA2RGB)
    #sys.stdout.buffer.write(b'Content-type: image/png\n\n')
    #output_rgba_array_to_stdout(im)
    #plt.savefig(sys.stdout.buffer, format='png')


    return 0

def plot_usa():

    # アメリカの州データを含むshapefileを読み込む
    usa = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    usa = usa[(usa.continent == 'North America') & (usa.name == 'United States of America')]
    
    # 地図上で州ごとにランダムな色を割り当てる
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))

    usa.boundary.plot(ax=ax)
    usa.plot(ax=ax, column='iso_a3', cmap='tab20', categorical=True, legend=True)
    plt.title('Map of USA with States Colored Randomly')
    plt.savefig('usa.png', bbox_inches='tight',dpi=300)


    #plt.show()
if __name__ == '__main__':

    stages = ["EMERGED",'BLOOMING','SETTING PODS','DROPPING LEAVS','HARVESTED']
    for stage in stages:
        plot_prog(stage)

    exit(0)
        #plot_usa()
    

    
