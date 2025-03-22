# Simple Dash app for displaying Virginia weather data

# By Kenneth Burchfiel
# Released under the MIT License

# Note: the Cloud Run-hosted copy of this app can be found 
# at https://simpleappwithoutlogin-470317599391.us-central1.run.app/ .

# (See readme for more information on the code used to connect
# to a Google Sheets workbook with recent weather data)

# Parts of the following code were based on the Dash app tutorial
# at https://dash.plotly.com/tutorial ; the Dash callbacks documentation at
# https://dash.plotly.com/basic-callbacks; the online Dash deployment
# guide at https://dash.plotly.com/deployment ; the Dash Bootstrap intro at
# https://dash-bootstrap-components.opensource.faculty.ai/docs/quickstart/ 
# ; and the Dash Bootstrap Layout documentation at
# https://dash-bootstrap-components.opensource
# .faculty.ai/docs/components/layout/ .

import gspread
from gspread_dataframe import get_as_dataframe
from dash import Dash, html, dcc, dash_table, callback, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta

# From https://pypi.org/project/gspread-dataframe/
print("Initializing gspread using service account key stored within \
Cloud Run secrets volume:")


local_data_import = False # This allows data to get imported from local
# .csv files, which can help save time when debugging. It must be 
# set to False prior to exporting the app to Cloud Run, however.

if local_data_import == False:
# Guillaume Blaquiere's post at 
# https://stackoverflow.com/a/68536068/13097194 
# was helpful in drafting the following line. 

    gc = gspread.service_account(
    filename='/svcacctsecret/kjb3server_service_account')
    wb = gc.open_by_key('17aDJ3mg49-n0IEnDgN7ZB85pO87fiUpkZPULYDB8dmo')

# Note: the code above will only run successfully when the app is
# deployed to Cloud Run. That's because the file path is actually a volume
# within my Cloud Run container.
# (See the readme for further details on successfully running
# this code on your end.)

# Importing data from each spreadsheet:
wx_df_list = []

for station in ['KCHO', 'KIAD', 'KOKV']:
    if local_data_import == True:
        wx_df_list.append(pd.read_csv(f'../../Updating_Online_\
Spreadsheets/weather_data/{station}_historical_hourly_data_\
updated.csv')[-960:])
    else:
        ws = wb.worksheet(station)
        wx_df_list.append(get_as_dataframe(ws)[-960:]) # Importing up to
        # 40 days of data for each station (in order to keep the charts
        # readable)

# Combining these station-specific tables into a single DataFrame:

df_wx = pd.concat([df for df in wx_df_list])

df_wx['Date/Time'] = pd.to_datetime(df_wx['Date/Time'])
print(df_wx.tail())

# Creating a condensed copy of df_wx for 
# incorporation in a DataTable:
# (This table will also be sorted in descending chronological order
# in order to display the most recent metrics first.)

current_date = datetime.today()

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# The dcc.Markdown() code below was based on
# https://dash.plotly.com/dash-core-components/markdown

app.layout = dbc.Container(
    [dbc.Row(dcc.Markdown('''
## Recent Weather Data for Three Virginia Airports
This Dash app is part of [Python for Nonprofits]\
(https://github.com/kburchfiel/pfn) and has been 
released under the MIT license. The source code for this app can 
be viewed at [this page](https://github.com/kburchfiel/pfn/blob/main/\
Online_Visualizations/Simple_App_Without_Login/app.py). 

The NWS data displayed within this notebook was accessed via
[this Google Sheets file](https://docs.google.com/spreadsheets/d/\
17aDJ3mg49-n0IEnDgN7ZB85pO87fiUpkZPULYDB8dmo/edit?gid=0#gid=0). 
This file gets updated with new NWS data
on an hourly basis via [this script](https://github.com/kburchfiel/\
pfn/blob/main/Updating_Online_Spreadsheets/\
updating_online_spreadsheets.py), which in turn calls 
[this script](https://github.com/kburchfiel/pfn/blob/main/\
Updating_Online_Spreadsheets/weather_import.py).

A more complex \
Dash app can be found within [this part of PFN]\
(https://github.com/kburchfiel/pfn/tree/main/\
Online_Visualizations/PFN_Dash_App_Demo).

    
    ''')),
dbc.Row([
    dbc.Col(
        dcc.Markdown('**Metric**:'), md = 2),
    dbc.Col(
        dcc.Dropdown(
    options = ['Temp', 'Dew Point', 
'1-Hour Precip', 'Rolling 3-Hour Precip', 'Rolling 6-Hour Precip',
'Rolling 12-Hour Precip', 'Rolling 24-Hour Precip',
'Altimeter (in.)', 'Windspeed'], value = 'Temp', id = 'metric'), 
        md = 3)]),
 dbc.Row([
     dbc.Col(dcc.Markdown('**Stations:**'), md = 2),
     dbc.Col(dcc.Dropdown(['KCHO', 'KIAD', 'KOKV'], 
                      ['KCHO', 'KIAD', 'KOKV'], 
                          multi=True,
                     id = 'station_list'),  md = 4)]),
dbc.Row([dbc.Col(dcc.Markdown('**Days to Include:**'), 
                md = 2),
        dbc.Col(dcc.Slider(1, 40, 3, value = 10, 
        # I had originally used one-day increments for the slider,
       # but this resulted in overlapping text on mobile displays.
                   id = 'days_to_include'))]),
dbc.Row(dcc.Graph(id = 'fig')),                                   
 dbc.Row(dcc.Markdown("By Kenneth Burchfiel"))])


# Defining a callback function that, given the inputs specified
# above, can plot and return a graph of weather data:
@callback(
    Output('fig', 'figure'),
    Input('metric', 'value'),
    Input('station_list', 'value'),
    Input('days_to_include', 'value'))

def plot_graph(metric, station_list, days_to_include):
    # Determining the earliest point at which data should be displayed:
    data_cutoff = str(current_date - timedelta(
        days = days_to_include))

    # Modifying the title so that it's gramatically correct when
    # only one day of data is being displayed:
    if days_to_include == 1:
        day_title_component = 'Past Day'
    else:
        day_title_component = f'Last {days_to_include} Days'
    
    fig = px.line(
        df_wx.query("(Station in @station_list) \
    & (`Date/Time` >= @data_cutoff)"), 
        x = 'Date/Time', y = metric,
        color = 'Station',
        title = f"{metric} Over {day_title_component}")
    
    # Updating y axis title based on the selected metric:
    fig.update_layout(xaxis_title = 'Date')
    if metric in ['Temp', 'Dew Point']:
        fig.update_layout(yaxis_title = 'Degrees (F)')
    if metric == 'Windspeed':
        fig.update_layout(yaxis_title = 'Windspeed (mph)')
    if 'Precip' in metric:
        fig.update_layout(yaxis_title = 'Precipitation (in.)')
    return fig


if __name__ == '__main__':
    app.run(debug=True)
