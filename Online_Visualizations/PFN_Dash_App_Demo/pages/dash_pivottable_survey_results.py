# This code shows how to use the dash-pivottable library to easily create 
# an interactive survey results dashboard.

# For additional documentation, see enrollment_pivot.py.


import dash
from dash import html, callback, Input, Output
import dash_pivottable
import pandas as pd

# Reading in survey data, then merging it with
# enrollment data:
# (The benefit of using original student-level data is that
# our averages will automatically be weighted by student counts, thus 
# producing more accurate averages.)

from data_import import df_survey_results_extra_data


lod_survey_results_extra_data = df_survey_results_extra_data.to_dict(
    orient = 'records')


dash.register_page(__name__, path = '/dash_pivottable_survey_results')

layout = html.Div([
    dash_pivottable.PivotTable(
        id='table',
        data=lod_survey_results_extra_data,
        cols=['Season'],
        colOrder="key_a_to_z",
        rows=['College'],
        rowOrder="key_a_to_z",
        rendererName="Grouped Column Chart",
        aggregatorName="Average",
        vals=["Score"],
        valueFilter={}
    ),
    html.Div(
        id='output'
    )
])


@callback(Output('output', 'children'),
              [Input('table', 'cols'),
               Input('table', 'rows'),
               Input('table', 'rowOrder'),
               Input('table', 'colOrder'),
               Input('table', 'aggregatorName'),
               Input('table', 'rendererName')])
def display_props(cols, rows, row_order, col_order, aggregator, renderer):
    return [
        html.P(str(cols), id='columns'),
        html.P(str(rows), id='rows'),
        html.P(str(row_order), id='row_order'),
        html.P(str(col_order), id='col_order'),
        html.P(str(aggregator), id='aggregator'),
        html.P(str(renderer), id='renderer'),
    ]