#!/usr/bin/env python
# coding: utf-8

# http://52.55.244.224:8501/

import pandas as pd
import numpy as np
from bokeh.io import output_file, output_notebook
from bokeh.plotting import figure, show
from bokeh.layouts import row, column, gridplot
from bokeh.models.widgets import Tabs, Panel
from bokeh.models import ColumnDataSource, CategoricalColorMapper, BasicTickFormatter, NumeralTickFormatter, HoverTool, DatetimeTickFormatter, CustomJS
# from bokeh.io import curdoc
# from bokeh.models import ColumnDataSource, Grid, LinearAxis, Plot, VBar
from bokeh.models import DataTable, DateFormatter, TableColumn, HTMLTemplateFormatter
from bokeh.models import ResetTool, BoxZoomTool, TapTool, BoxSelectTool, HoverTool
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

    prim_color = st.config.get_option('theme.primaryColor') or '#f43365'
    bg_color = st.config.get_option('theme.backgroundColor') or '#000000'
    sbg_color = st.config.get_option('theme.secondaryBackgroundColor') or '#f1f3f6'
    txt_color = st.config.get_option('theme.textColor') or '#000000' 
    font = st.config.get_option('theme.font') or 'sans serif'  
    border_color = '#cccccc'
	
    custom_css = f"""
        <style>
            #{button_id} {{
                background-color: {sbg_color};
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

#     custom_css = f"""
#         <style>
#             #{button_id} {{
#                 background-color: {bg_color};
#                 color: {txt_color};
#                 padding: 0.25rem 0.75rem;
#                 position: relative;
#                 line-height: 1.6;
#                 border-radius: 0.25rem;
#                 border-width: 1px;
#                 border-style: solid;
#                 border-color: {border_color};
#                 border-image: initial;
#                 filter: brightness(105%);
#                 justify-content: center;
#                 margin: 0px;
#                 width: auto;
#                 appearance: button;
#                 display: inline-flex;
#                 family-font: {font};
#                 font-weight: 400;
#                 letter-spacing: normal;
#                 word-spacing: normal;
#                 text-align: center;
#                 text-rendering: auto;
#                 text-transform: none;
#                 text-indent: 0px;
#                 text-shadow: none;
#                 text-decoration: none;
#             }}
#             #{button_id}:hover {{
                
#                 border-color: {prim_color};
#                 color: {prim_color};
#             }}
#             #{button_id}:active {{
#                 box-shadow: none;
#                 background-color: {prim_color};
#                 color: {sbg_color};
#                 }}
#         </style> """

    dl_link = (
        custom_css
        + f'<a download="{file_name}" id="{button_id}" href="data:file/{file_type};base64,{b64}">Download raw data for {month}.{day}.{year}</a><br></br>'
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

date = datetime.datetime.now()
yesterday = date - datetime.timedelta(days=1)

# print(date)
firstOfThisMonth = yesterday.replace(day=1)
# print(firstOfThisMonth)
endOfLastMonth = firstOfThisMonth - datetime.timedelta(days=1)
# print(endOfLastMonth)
firstOfLastMonth = endOfLastMonth.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

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

# st.sidebar.header("Select Syncronization Date")
# date = st.sidebar.date_input('Date', value=max(dates), min_value=min(dates), max_value=max(dates))
date = st.sidebar.date_input('Select Syncronization Date', value=max(dates), min_value=min(dates), max_value=max(dates))
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
    df1 = pd.read_excel(io.BytesIO(obj['Body'].read()), engine='openpyxl', sheet_name='customers_raw_data', parse_dates=['Date'])
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

min_date = min(df2['Activity_Date__c'].min(), df3['Completion_Walk_Date__c'].min(), df4['Last_Install_Completion_Date__c'].min())

value = st.sidebar.radio('Select Period of Report', ['This and Last Months', 'All Data'])

if value == 'This and Last Months':
    start = firstOfLastMonth
else:
    start = min_date

# df1 = df1.loc[df1['Date'] >= start]
df1 = df1.loc[df1['Created'] == 'N']
df1 = df1.sort_values('Date')
df1.reset_index(inplace=True, drop=True)
df1.index = df1.index + 1
df1.reset_index(inplace=True)
# print(df1)

df1r = df1[['Date', 'Id']].set_index('Date')
df1r = df1r.resample('D').count()
df1r.reset_index(inplace=True)

source_1 = ColumnDataSource(df1r)
source = ColumnDataSource(df1)

TOOLS = "box_zoom, reset"
fig_1 = figure(plot_height=int(plot_height), plot_width=plot_width, 
               title="Number of Missing Customers by Dates",
               tools=TOOLS,
               toolbar_location='above')

# width = 0.2 * (max(temp_df['Date']) - min(temp_df['Date'])).total_seconds() * 1000 / len(temp_df['Date'])
# width = 0.2 * (max(df1['Date']) - min(df1['Date'])).total_seconds() * 1000 / len(df1['Date'])
width = 0.9 * 24 * 60 * 60 * 1000

# fig_1.vbar(x=temp_df.Date, top=temp_df.attributes, width=width)
fig_1.vbar(x='Date', top='Id', source=source_1, width=width)
# fig_1.vbar(x='Date', top='Id', source=source, width=width)

fig_1.y_range.start = 0
fig_1.xgrid.grid_line_color = None
fig_1.axis.minor_tick_line_color = None
fig_1.outline_line_color = None
fig_1.xaxis.axis_label = 'Date'
fig_1.yaxis.axis_label = 'Customers'
fig_1.xaxis.formatter = DatetimeTickFormatter(days="%b %d, %Y",
                                              months="%b %d, %Y",)
# fig_1.select_one(HoverTool).tooltips = [('Number of Customers', '@top{int}')]

columns = [
	TableColumn(field="index", title="#", width=int(plot_width/16)),
        TableColumn(field="Date", title="Date", formatter=DateFormatter(), width=int(plot_width*2/16)),
	TableColumn(field="link", title="Link", formatter=HTMLTemplateFormatter(template='<a href="<%= value %>" target="_blank" rel="noopener"><%= value %></a>'), width=int(plot_width*13/16))
    ]
data_table = DataTable(source=source, columns=columns, width=plot_width, height=int(plot_height/2), index_position=None)

df2 = df2.loc[df2['Activity_Date__c'] >= start]
df2 = df2.sort_values('Activity_Date__c', ascending=False)
# Store the data in a ColumnDataSource
s1 = ColumnDataSource(data=dict(x=df2['Activity_Date__c'], y=df2['HEA_Invoice_Amount__c'], z=df2['Created'],
			        a=df2['HEA_Revenue_Total__c'], b=df2['link']))
# s2 = ColumnDataSource(data=dict(x=df2['Activity_Date__c'], y=df2['HEA_Invoice_Amount__c'], z=df2['Created'],
# 			         a=df2['HEA_Revenue_Total__c'], b=df2['link']))
s2 = ColumnDataSource(data=dict(x=[], y=[], z=[],
			        a=[], b=[]))

# Create a CategoricalColorMapper that assigns specific colors to Y and N
created_mapper = CategoricalColorMapper(factors=['Y', 'N'], 
                                        palette=['#008000', '#FF0000'])

# Specify the tools
toolList = ["lasso_select", 'hover', 'box_zoom', 'reset', 'tap']

toolList2 = [ResetTool(), BoxZoomTool(), TapTool(), BoxSelectTool(), HoverTool()]

# Create a figure 
amountFig = figure(title='Invoice Amounts', x_axis_type='datetime',
                   plot_height=int(plot_height/2), plot_width=plot_width, 
                   tools=toolList, 
# 		   toolbar_location="right",
#                    aspect_ratio=16/9,
                   x_axis_label='Date', y_axis_label='Invoice Amount')

# Draw with circle markers
# amountFig.circle(x='Activity_Date__c', y='HEA_Invoice_Amount__c', 
amountFig.circle(x='x', y='y', 
                 source=s1,  fill_alpha=0.6,
                 size=5, color=dict(field='z', 
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
                    plot_height=int(plot_height/2), plot_width=plot_width, 
		    tools=toolList,
                    x_axis_label='Date', y_axis_label='Total Revenue',
# 		    toolbar_location=None, 
            	    x_range=amountFig.x_range, y_range=amountFig.y_range)

# Draw with square markers
# revenueFig.square(x='Activity_Date__c', y='HEA_Revenue_Total__c', 
revenueFig.square(x='x', y='a', 
                  source=s1, size=5, fill_alpha=0.6,
                  color=dict(field='z', transform=created_mapper)
# 		  , legend_field="Created"
		 )
# revenueFig.legend.orientation = "vertical"
# revenueFig.legend.location = "top_left"
# revenueFig.legend.click_policy="hide"
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

# columns_hea = [
# # 	TableColumn(field="index", title="#", width=int(plot_width/16)),
#         TableColumn(field="Activity_Date__c", title="Date", formatter=DateFormatter(), width=int(plot_width*2/16)),
# 	TableColumn(field="HEA_Invoice_Amount__c", title="Amount", width=int(plot_width/16)),
# 	TableColumn(field="link", title="Link", formatter=HTMLTemplateFormatter(template='<a href="<%= value %>" target="_blank" rel="noopener"><%= value %></a>'), width=int(plot_width*13/16))
#     ]
columns_hea = [
# 	TableColumn(field="index", title="#", width=int(plot_width/16)),
        TableColumn(field="x", title="Date", formatter=DateFormatter(), width=int(plot_width*2/16)),
	TableColumn(field="y", title="Amount", width=int(plot_width/16)),
	TableColumn(field="b", title="Link", formatter=HTMLTemplateFormatter(template='<a href="<%= value %>" target="_blank" rel="noopener"><%= value %></a>'), width=int(plot_width*13/16))
    ]
data_table_hea = DataTable(source=s2, columns=columns_hea, width=plot_width, height=int(plot_height/2), 
# 			   index_position=None, 
			   sortable=True, selectable=True, editable=True)

s1.selected.js_on_change(
    "indices",
    CustomJS(
        args=dict(s1=s1, s2=s2, table=data_table_hea),
        code="""
        var inds = cb_obj.indices;
        var d1 = s1.data;
        var d2 = s2.data;
        d2['x'] = []
        d2['y'] = []
	d2['z'] = []
	d2['a'] = []
	d2['b'] = []
        for (var i = 0; i < inds.length; i++) {
            d2['x'].push(d1['x'][inds[i]])
            d2['y'].push(d1['y'][inds[i]])
	    d2['z'].push(d1['z'][inds[i]])
	    d2['a'].push(d1['a'][inds[i]])
	    d2['b'].push(d1['b'][inds[i]])
        }
        s2.change.emit();
        table.change.emit();

        var inds = source_data.selected.indices;
        var data = source_data.data;
        var out = "x, y, z, a, b\\n";
        for (i = 0; i < inds.length; i++) {
            out += data['x'][inds[i]] + "," + data['y'][inds[i]] + "," + data['z'][inds[i]] + "," + data['a'][inds[i]] + "," + data['b'][inds[i]]+ "\\n";
        }
        var file = new Blob([out], {type: 'text/plain'});

    """,
    ),
)

df3 = df3.loc[df3['Completion_Walk_Date__c'] >= start]
df3 = df3.sort_values('Completion_Walk_Date__c', ascending=False)
# Store the data in a ColumnDataSource
data_cds = ColumnDataSource(df3)

# Create a figure 
wx_lv_Fig = figure(title='LV Invoice Amounts', x_axis_type='datetime',
                   plot_height=int(plot_height/2), plot_width=plot_width, tools=toolList2, 
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
                     plot_height=int(plot_height/2), plot_width=plot_width, 
		     tools=toolList2,
                     x_axis_label='Date', y_axis_label='Customer Invoice Amount',
		     toolbar_location=None, 
            	     x_range=wx_lv_Fig.x_range, 
# 		     y_range=wx_lv_Fig.y_range
		    )

# Draw with circle markers
wx_cust_Fig.circle(x='Completion_Walk_Date__c', y='Wx_Gross_Sale__c', 
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

columns_wx = [
# 	TableColumn(field="index", title="#", width=int(plot_width/16)),
        TableColumn(field="Completion_Walk_Date__c", title="Date", formatter=DateFormatter(), width=int(plot_width*2/16)),
	TableColumn(field="Total_Cost_to_RISE__c", title="LV Invoice Amount", width=int(plot_width*2/16)),
	TableColumn(field="Wx_Gross_Sale__c", title="Customer Invoice Amount", width=int(plot_width*2/16)),
	TableColumn(field="link", title="Link", formatter=HTMLTemplateFormatter(template='<a href="<%= value %>" target="_blank" rel="noopener"><%= value %></a>'), width=int(plot_width*10/16))
    ]
data_table_wx = DataTable(source=data_cds, columns=columns_wx, width=plot_width, height=int(plot_height/2), index_position=None)

df4 = df4.loc[df4['Last_Install_Completion_Date__c'] >= start]
df4 = df4.sort_values('Last_Install_Completion_Date__c', ascending=False)
# Store the data in a ColumnDataSource
data_cds = ColumnDataSource(df4)

# Create a figure 
hvac_Fig = figure(title='Contract Price', x_axis_type='datetime',
                  plot_height=plot_height, plot_width=plot_width, tools=toolList2, 
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

columns_hvac = [
# 	TableColumn(field="index", title="#", width=int(plot_width/16)),
        TableColumn(field="Last_Install_Completion_Date__c", title="Date", formatter=DateFormatter(), width=int(plot_width*4/16)),
	TableColumn(field="Final_Contract_Price__c", title="Amount", width=int(plot_width*4/16)),
	TableColumn(field="link", title="HVAC Contract ID", formatter=HTMLTemplateFormatter(template='<a href="<%= value %>" target="_blank" rel="noopener"><%= Id %></a>'), 
		    width=int(plot_width*8/16))
    ]
data_table_hvac = DataTable(source=data_cds, columns=columns_hvac, width=plot_width, height=int(plot_height/2), index_position=None)

# Create four panels
cust_panel = Panel(child=gridplot([[fig_1], [data_table]], sizing_mode='stretch_width'), title='Customers')
hea_panel = Panel(child=gridplot([[amountFig], [revenueFig], [data_table_hea]], sizing_mode='stretch_width'), title='HEA')
wx_panel = Panel(child=gridplot([[wx_lv_Fig], [wx_cust_Fig], [data_table_wx]], sizing_mode='stretch_width'), title='Wx')
hvac_panel = Panel(child=gridplot([[hvac_Fig], [data_table_hvac]], sizing_mode='stretch_width'), title='HVAC')

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


