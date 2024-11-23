# Simple Dash app for displaying weather data

# Note: the Cloud Run-hosted copy of this app can be found 
# at https://simpleappwithoutlogin-470317599391.us-central1.run.app/ .

# (See readme for more information on the code used to connect
# to a Google Sheets workbook with recent weather data)

# By Kenneth Burchfiel
# Released under the MIT License

# Parts of the following code were based on the Dash app tutorial
# at https://dash.plotly.com/tutorial ; the online Dash deployment
# guide at https://dash.plotly.com/deployment ; the Dash Bootstrap intro at
# https://dash-bootstrap-components.opensource.faculty.ai/docs/quickstart/ 
# ; and the Dash Bootstrap Layout documentation at
# https://dash-bootstrap-components.opensource
# .faculty.ai/docs/components/layout/ .

import gspread
from gspread_dataframe import get_as_dataframe
from dash import Dash, html, dcc, dash_table
import plotly.express as px
import pandas as pd
import dash
import dash_bootstrap_components as dbc

# From https://pypi.org/project/gspread-dataframe/
print("Initializing gspread using service account key stored within \
Cloud Run secrets volume:")

# Note: the following code will only run when the app is deployed to
# Cloud Run. That's because the file path is actually a volume
# within my Cloud Run container. However, the file can be run locally
# by replacing this path with a path to my local service account.
# (See the readme for further details on successfully running
# this code on your end.)

# Guillaume Blaquiere's post at 
# https://stackoverflow.com/a/68536068/13097194 
# was helpful in drafting the following line. 

gc = gspread.service_account(
filename='/svcacctsecret/kjb3server_service_account'

wb = gc.open_by_key('17aDJ3mg49-n0IEnDgN7ZB85pO87fiUpkZPULYDB8dmo')
ws = wb.worksheet('KCHO')
df_wx = get_as_dataframe(ws)[-1000:] # Limits the output to the last
# ~41 days in order to make the charts more readable
print(df_wx.tail())

# Creating a condensed copy of df_wx for 
# incorporation in a DataTable:
# (This table will also be sorted in descending chronological order
# in order to display the most recent metrics first.)

df_wx_condensed = df_wx[
['Date/Time', 'Temp', '1-Hour Precip', '3-Hour Precip', '6-Hour Precip', 
 'Weather', 'Dew Point', 'Wind (mph)', 'Time Zone']].copy().sort_values(
    'Date/Time', ascending = False)


station_code = 'KCHO'

# temp_df = pd.DataFrame(data = {'x':[1, 2, 3, 4], 'y':[0, 3, 9, 7]})

# fig_temp = px.line(temp_df, x = 'x', y = 'y')
# fig_precip = px.line(temp_df, x = 'x', y = 'y')

fig_temp = px.line(
    df_wx, x = 'Date/Time', y = ['Temp', 'Dew Point'],
       title = f'{station_code} Temperature and \
Dew Point')
fig_temp.update_layout(yaxis_title = 'Degrees (F)')

fig_precip = px.bar(df_wx.query('`1-Hour Precip` > 0.0'),
                   x = 'Date/Time', y = '1-Hour Precip',
       title = f'{station_code} Hourly Precipitation<br><sub>Note: to \
make the bars easier to view, hours without any precipitation are \
excluded from this chart.',
                  text_auto = '.2f')
fig_precip.update_layout(yaxis_title = 'Precipitation (in.)')
fig_precip.update_xaxes(type = 'category')

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# The dcc.Markdown() code below was based on
# https://dash.plotly.com/dash-core-components/markdown

app.layout = dbc.Container(
    [dbc.Row(dcc.Markdown('''
    ## Recent Charlottesville, VA weather data
    This Dash app is part of [Python for Nonprofits]\
(https://github.com/kburchfiel/pfn) and has been \
released under the MIT license. The source code for this app can \
be viewed at [this page](https://github.com/kburchfiel/pfn/tree/\
main/Online_Visualizations/Simple_App_Without_Login). A more complex \
Dash app can be found within [this part of PFN]\
(https://github.com/kburchfiel/pfn/tree/main/\
Online_Visualizations/PFN_Dash_App_Demo).

    
    ''')),
              dbc.Row(dcc.Graph(figure=fig_temp)),
             dbc.Row(dcc.Graph(figure=fig_precip)),
             dbc.Row(dash_table.DataTable(
                 df_wx_condensed.to_dict('records'), 
                 [{"name": i, "id": i} for i in df_wx_condensed.columns],
             sort_action="native")),
             dbc.Row(dcc.Markdown("By Kenneth Burchfiel"))])

# The dash_table entry was based on
# https://dash.plotly.com/datatable and
# https://dash.plotly.com/datatable/interactivity .

if __name__ == '__main__':
    app.run(debug=True)