#!/usr/bin/env python
# coding: utf-8

# http://52.55.244.224:8501/

import pandas as pd
from bokeh.io import output_file, output_notebook
from bokeh.plotting import figure, show
from bokeh.layouts import row, column, gridplot
from bokeh.models.widgets import Tabs, Panel
from bokeh.models import ColumnDataSource, CategoricalColorMapper, BasicTickFormatter, NumeralTickFormatter, HoverTool, DatetimeTickFormatter
import datetime
import boto3
import io
import streamlit as st
from PIL import Image
import re
import base64
import uuid


def download_aws_object(bucket, key):
    """
    Download an object from AWS
    Example key: my/key/some_file.txt
    """
    s3 = boto3.resource('s3')
    obj = s3.Object(bucket, key)
    file_name = key.split('/')[-1] # e.g. some_file.txt
    file_type = file_name.split('.')[-1] # e.g. txt
    b64 = base64.b64encode(obj.get()['Body'].read()).decode()

    button_uuid = str(uuid.uuid4()).replace("-", "")
    button_id = re.sub("\d+", "", button_uuid)

#     custom_css = f""" 
#         <style>
#             #{button_id} {{
#                 background-color: rgb(255, 255, 255);
#                 color: rgb(38, 39, 48);
#                 padding: 0.25em 0.38em;
#                 position: relative;
#                 text-decoration: none;
#                 border-radius: 4px;
#                 border-width: 1px;
#                 border-style: solid;
#                 border-color: rgb(230, 234, 241);
#                 border-image: initial;
#             }} 
#             #{button_id}:hover {{
#                 border-color: rgb(246, 51, 102);
#                 color: rgb(246, 51, 102);
#             }}
#             #{button_id}:active {{
#                 box-shadow: none;
#                 background-color: rgb(246, 51, 102);
#                 color: white;
#                 }}
#         </style> """

    prim_color = st.config.get_option('theme.primaryColor') or '#F43365'
#     bg_color = st.config.get_option('theme.backgroundColor') or '#000000'
    btn_bg_color = '#F3F6FC'
    border_color = '#DADFE7'
    sbg_color = st.config.get_option('theme.secondaryBackgroundColor') or '#f1f3f6'
    txt_color = st.config.get_option('theme.textColor') or '#000000' 
    font = st.config.get_option('theme.font') or 'sans serif'  

    custom_css = f"""
        <style>
            #{button_id} {{
                background-color: {btn_bg_color};
                color: {txt_color};
                padding: 0.25rem 0.75rem;
                position: relative;
                line-height: 1.6;
                border-radius: 0.25rem;
                border-width: 1px;
                border-style: solid;
                border-color: {border_color};
                border-image: initial;
                filter: brightness(105%);
                justify-content: center;
                margin: 0px;
                width: auto;
                appearance: button;
                display: inline-flex;
                family-font: {font};
                font-weight: 400;
                letter-spacing: normal;
                word-spacing: normal;
                text-align: center;
                text-rendering: auto;
                text-transform: none;
                text-indent: 0px;
                text-shadow: none;
                text-decoration: none;
            }}
            #{button_id}:hover {{
                
                border-color: {prim_color};
                color: {prim_color};
            }}
            #{button_id}:active {{
                box-shadow: none;
                background-color: {prim_color};
                color: {sbg_color};
                }}
        </style> """

    dl_link = (
        custom_css
        + f'<a download="{file_name}" id="{button_id}" href="data:file/{file_type};base64,{b64}">Download file "{file_name}"</a><br></br>'
    )
    return dl_link

output_file(filename="report.html", title="Report")

plot_height = 500
plot_width = 800

im = Image.open("image.jpeg")
st.set_page_config(
    page_title="Missing Customers & Invoices",
    page_icon=im,
#     layout="wide",
)

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

padding = 0
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)

# date = datetime.datetime.now()

bucket = "celigo-df-check"

session = boto3.Session()
s3resource = session.resource('s3')
bucket_r = s3resource.Bucket(bucket)
prefix = ''
objects = bucket_r.objects.filter(Prefix=prefix)
# print(len(list(objects)))

s3 = boto3.client('s3')

pattern = re.compile(r'Celigo - [0-9.]+.xlsx')
files_lst = []
for object in objects:
    if pattern.match(object.key):
#         print(object.key)
        files_lst.append(object.key)

# print(files_lst)
# print(len(files_lst))

dates = [datetime.datetime.strptime(f"{e.split(' ')[2].split('.')[2]}-{e.split(' ')[2].split('.')[0]}-{e.split(' ')[2].split('.')[1]}", '%Y-%m-%d') for e in files_lst]
# print(dates)
# print(max(dates))

# st.sidebar.header("Select a Date")
# date = st.sidebar.date_input('Date', value=max(dates), min_value=min(dates), max_value=max(dates))
date = st.sidebar.date_input('Select a Date', value=max(dates), min_value=min(dates), max_value=max(dates))
# st.write(date)

# i = 0
# while i < 10:
#     try:
#         year = date.strftime('%Y')
#         month = date.strftime('%m').zfill(2)
#         day = date.strftime('%d').zfill(2)
#         file_name = f'Celigo - {month}.{day}.{year}.xlsx'
#         obj = s3.get_object(Bucket=bucket, Key=file_name)
#         print(f'file {file_name} is downloaded')
#         break
#     except Exception as e:
#         print(e)
#         print(date)
#         date = date - datetime.timedelta(days=1)
#         i += 1

try:
    year = date.strftime('%Y')
    month = date.strftime('%m').zfill(2)
    day = date.strftime('%d').zfill(2)
    file_name = f'Celigo - {month}.{day}.{year}.xlsx'
    obj = s3.get_object(Bucket=bucket, Key=file_name)
    print(f'file {file_name} is downloaded')
except Exception as e:
    print(e)
    print(date)
#     st.write('Data for the selected date does not exist. Please choose another date')
    st.error("Data for the selected date does not exist. Please choose another date.")
    st.stop()
    
try:
    temp_df = pd.read_excel(io.BytesIO(obj['Body'].read()), engine='openpyxl', sheet_name='customers', parse_dates=['Date'])
except Exception as e:
    print(e)

try:
    obj = s3.get_object(Bucket=bucket, Key=file_name)
    df2 = pd.read_excel(io.BytesIO(obj['Body'].read()), engine='openpyxl', sheet_name='hea_invoices', parse_dates=['TS_HEA_Invoice_Submitted__c', 
                                                                                                                   'Activity_Date__c'])
except Exception as e:
    print(e)

try:
    obj = s3.get_object(Bucket=bucket, Key=file_name)
    df3 = pd.read_excel(io.BytesIO(obj['Body'].read()), engine='openpyxl', sheet_name='wx_invoices', parse_dates=['Completion_Walk_Date__c'])
except Exception as e:
    print(e)

try:
    obj = s3.get_object(Bucket=bucket, Key=file_name)
    df4 = pd.read_excel(io.BytesIO(obj['Body'].read()), engine='openpyxl', sheet_name='hvac_invoices', parse_dates=['Last_Install_Completion_Date__c'])
except Exception as e:
    print(e)

TOOLS = "hover, pan, box_zoom, reset, wheel_zoom, tap"
fig_1 = figure(plot_height=plot_height, plot_width=plot_width, 
               title="Number of Missing Customers by Dates",
               tools=TOOLS,
               toolbar_location='above')

width = 0.2 * (max(temp_df['Date']) - min(temp_df['Date'])).total_seconds() * 1000 / len(temp_df['Date'])

fig_1.vbar(x=temp_df.Date, top=temp_df.attributes, width=width)

fig_1.y_range.start = 0
fig_1.xgrid.grid_line_color = None
fig_1.axis.minor_tick_line_color = None
fig_1.outline_line_color = None
fig_1.xaxis.axis_label = 'Date'
fig_1.yaxis.axis_label = 'Customers'
fig_1.xaxis.formatter = DatetimeTickFormatter(days="%b %d, %Y",
                                              months="%b %d, %Y",)
fig_1.select_one(HoverTool).tooltips = [('Number of Customers', '@top{int}')]

# Store the data in a ColumnDataSource
data_cds = ColumnDataSource(df2)

# Create a CategoricalColorMapper that assigns specific colors to Y and N
created_mapper = CategoricalColorMapper(factors=['Y', 'N'], 
                                        palette=['Green', 'Red'])

# Specify the tools
toolList = ['hover', 'pan', 'box_zoom', 'reset', 'wheel_zoom', 'tap', 'lasso_select']

# Create a figure 
amountFig = figure(title='Invoice Amounts', x_axis_type='datetime',
                   plot_height=int(plot_height/2), plot_width=plot_width, 
                   tools=toolList, 
#                    aspect_ratio=16/9,
                   x_axis_label='Date', y_axis_label='Invoice Amount')

# Draw with circle markers
amountFig.circle(x='Activity_Date__c', y='HEA_Invoice_Amount__c', 
                 source=data_cds,  fill_alpha=0.6,
                 size=5, color=dict(field='Created', 
                                    transform=created_mapper))
amountFig.xgrid.grid_line_color = None
amountFig.axis.minor_tick_line_color = None
amountFig.outline_line_color = None

hover = amountFig.select(dict(type=HoverTool))
tips = [('Date','$x{%F}'), ('Amount','$y{0.2f}')]
hover.tooltips = tips
hover.mode = 'mouse'
hover.formatters = {"$x": "datetime"}

# Format the y-axis tick labels 
# amountFig.yaxis[0].formatter = NumeralTickFormatter(format='0000')
amountFig.xaxis.formatter = DatetimeTickFormatter(days="%b %d, %Y",
                                                  months="%b %d, %Y",)

# Create a figure relating the totals
revenueFig = figure(title='Total Revenues', x_axis_type='datetime', 
                    plot_height=int(plot_height/2), plot_width=plot_width, tools=toolList,
                    x_axis_label='Date', y_axis_label='Total Revenue')

# Draw with square markers
revenueFig.square(x='Activity_Date__c', y='HEA_Revenue_Total__c', 
                  source=data_cds, size=5, fill_alpha=0.6,
                  color=dict(field='Created', transform=created_mapper))
revenueFig.xgrid.grid_line_color = None
revenueFig.axis.minor_tick_line_color = None
revenueFig.outline_line_color = None

hover_r = revenueFig.select(dict(type=HoverTool))
tips_r = [('Date','$x{%F}'), ('Revenue','$y{0.2f}')]
hover_r.tooltips = tips_r
hover_r.mode = 'mouse'
hover_r.formatters = {"$x": "datetime"}

revenueFig.xaxis.formatter = DatetimeTickFormatter(days="%b %d, %Y",
                                                   months="%b %d, %Y",)
# Store the data in a ColumnDataSource
data_cds = ColumnDataSource(df3)

# Create a figure 
wx_lv_Fig = figure(title='LV Invoice Amounts', x_axis_type='datetime',
                   plot_height=int(plot_height/2), plot_width=plot_width, tools=toolList, 
                   x_axis_label='Date', y_axis_label='LV Invoice Amount')

# Draw with circle markers
wx_lv_Fig.circle(x='Completion_Walk_Date__c', y='Total_Cost_to_RISE__c', 
                 source=data_cds, fill_alpha=0.6,
                 size=5, color=dict(field='Created', 
                                    transform=created_mapper))
wx_lv_Fig.xgrid.grid_line_color = None
wx_lv_Fig.axis.minor_tick_line_color = None
wx_lv_Fig.outline_line_color = None

hover = wx_lv_Fig.select(dict(type=HoverTool))
tips = [('Date','$x{%F}'), ('Amount','$y{0.2f}')]
hover.tooltips = tips
hover.mode = 'mouse'
hover.formatters = {"$x": "datetime"}

wx_lv_Fig.xaxis.formatter = DatetimeTickFormatter(days="%b %d, %Y",
                                                  months="%b %d, %Y",)

# Create a figure 
wx_cust_Fig = figure(title='Customer Invoice Amounts', x_axis_type='datetime', 
                     plot_height=int(plot_height/2), plot_width=plot_width, tools=toolList,
                     x_axis_label='Date', y_axis_label='Customer Invoice Amount')

# Draw with square markers
wx_cust_Fig.square(x='Completion_Walk_Date__c', y='Wx_Gross_Sale__c', 
                   source=data_cds, size=5, fill_alpha=0.6,
                   color=dict(field='Created', transform=created_mapper))
wx_cust_Fig.xgrid.grid_line_color = None
wx_cust_Fig.axis.minor_tick_line_color = None
wx_cust_Fig.outline_line_color = None

hover_r = wx_cust_Fig.select(dict(type=HoverTool))
tips_r = [('Date','$x{%F}'), ('Amount','$y{0.2f}')]
hover_r.tooltips = tips_r
hover_r.mode = 'mouse'
hover_r.formatters = {"$x": "datetime"}

wx_cust_Fig.xaxis.formatter = DatetimeTickFormatter(days="%b %d, %Y",
                                                    months="%b %d, %Y",)

# Store the data in a ColumnDataSource
data_cds = ColumnDataSource(df4)

# Create a figure 
hvac_Fig = figure(title='Contract Price', x_axis_type='datetime',
                  plot_height=plot_height, plot_width=plot_width, tools=toolList, 
                  x_axis_label='Date', y_axis_label='Contract Price')

# Draw with circle markers
hvac_Fig.circle(x='Last_Install_Completion_Date__c', y='Final_Contract_Price__c', 
                source=data_cds, fill_alpha=0.6,
                size=5, color=dict(field='Created', 
                                   transform=created_mapper))
hvac_Fig.xgrid.grid_line_color = None
hvac_Fig.axis.minor_tick_line_color = None
hvac_Fig.outline_line_color = None

hover = hvac_Fig.select(dict(type=HoverTool))
tips = [('Date','$x{%F}'), ('Amount','$y{0.2f}')]
hover.tooltips = tips
hover.mode = 'mouse'
hover.formatters = {"$x": "datetime"}

hvac_Fig.xaxis.formatter = DatetimeTickFormatter(days="%b %d, %Y",
                                                 months="%b %d, %Y",)

# Create four panels
cust_panel = Panel(child=gridplot([[fig_1], ], sizing_mode='stretch_both'), title='Customers')
hea_panel = Panel(child=gridplot([[amountFig], [revenueFig]], sizing_mode='stretch_both'), title='HEA')
wx_panel = Panel(child=gridplot([[wx_lv_Fig], [wx_cust_Fig]], sizing_mode='stretch_both'), title='Wx')
hvac_panel = Panel(child=gridplot([[hvac_Fig], ], sizing_mode='stretch_both'), title='HVAC')

# Assign the panels to Tabs
tabs = Tabs(tabs=[cust_panel, hea_panel, wx_panel, hvac_panel])

# Show the tabbed layout
st.bokeh_chart(tabs, use_container_width=False)

show(tabs)

with open('report.html', 'rb') as f:
	if st.sidebar.download_button('Download Report', f, file_name=f'Report - {month}.{day}.{year}.html'):
		st.write('Report downloaded')
    
# if st.sidebar.download_button('Download Report', data='report.html'):
# 	st.write('Report downloaded')
	
st.sidebar.markdown(download_aws_object(bucket, file_name), unsafe_allow_html=True)
