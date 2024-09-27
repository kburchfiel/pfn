# This code shows how to use the dash-pivottable library to easily 
# create an interactive enrollment dashboard.

# Much of this code derives from 
# https://github.com/plotly/dash-pivottable/blob/master/usage.py
# and https://dash.plotly.com/urls .


import dash
from dash import html, callback, Input, Output
import dash_pivottable
import pandas as pd
from data_import import df_curr_enrollment

# Reading in enrollment data:

# df_curr_enrollment = pd.read_csv(
#     'https://raw.githubusercontent.com/kburchfiel/\
# pfn/main/Appendix/curr_enrollment.csv')


# Note that the 'data' entry below should take the form of a list of lists
# or list of dicts, rather than a DataFrame. (For reference, see
# https://github.com/plotly/react-pivottable/#accepted-formats-for-data)
# Therefore, we'll need to convert our DataFrame into this format
# before we can run the code.
# It's possible to convert a DataFrame into a list of lists,
# but I believe the easiest solution is to use to_dict(orient = 'records')
# to convert the DataFrame into a list of dictionaries.

lod_curr_enrollment = df_curr_enrollment.to_dict(
    orient = 'records')
# lod = 'list of dicts'


dash.register_page(__name__, path = '/dash_pivottable_enrollment') # 

layout = html.Div([
    dash_pivottable.PivotTable(
        id='enrollment_table',
        data=lod_curr_enrollment,
        cols=['Level For Sorting', 'Level'],
        colOrder="key_a_to_z",
        rows=['College'],
        rowOrder="key_a_to_z",
        rendererName="Grouped Column Chart",
        aggregatorName="Sum",
        vals=["Enrollment"],
        valueFilter={}
    ),
    html.Div(
        id='output'
    )
])


@callback(Output('enrollment_output', 'enrollment_children'),
              [Input('enrollment_table', 'cols'),
               Input('enrollment_table', 'rows'),
               Input('enrollment_table', 'rowOrder'),
               Input('enrollment_table', 'colOrder'),
               Input('enrollment_table', 'aggregatorName'),
               Input('enrollment_table', 'rendererName')])
def display_props(cols, rows, row_order, col_order, aggregator, renderer):
    return [
        html.P(str(cols), id='columns'),
        html.P(str(rows), id='rows'),
        html.P(str(row_order), id='row_order'),
        html.P(str(col_order), id='col_order'),
        html.P(str(aggregator), id='aggregator'),
        html.P(str(renderer), id='renderer'),
    ]