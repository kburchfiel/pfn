# Flexible Survey Results Dashboard
# By Kenneth Burchfiel
# Released under the MIT License

# Parts of this code derive from
# and https://dash.plotly.com/urls 
# and https://dash.plotly.com/minimal-app .

# For a bit more documentation on this code, reference
# flexible_enrollment_dashboard.py, which uses a very similar setup.

import dash
from dash import html, dcc, callback, Output, Input
from data_import import df_survey_results_extra_data
import plotly.express as px
import dash_bootstrap_components as dbc
from auto_pivot_and_graph import autopivot_plus_bar

dash.register_page(__name__, path='/flexible_survey_results_dashboard')

# Configuring the page's layout:
layout = dbc.Container([
    dbc.Row(dbc.Col(dcc.Markdown('''
    # Flexible Interactive Survey Results Dashboard
    
    This dashboard provides a flexible overview of NVCU student survey 
    results. It utilizes the autopivot() and autobar() functions found 
    within auto_pivot_and_graph.py to allow for a wide range of 
    display options.
    '''), lg=9)),
    dbc.Row([
        dbc.Col(html.H5("Comparison Options:"), lg=3),
    dbc.Col(dcc.Dropdown(
        ['Starting Year', 'Season', 'Gender', 'Matriculation Year',
       'College', 'Class Of', 'Level', 'Level For Sorting'], 
        ['College', 'Season'], multi=True,
                 id='flexible_survey_results_index'), lg=3),
        dbc.Col(html.H5("Color Option:"), lg=2),
    dbc.Col(dcc.Dropdown(
        ['Starting Year', 'Season', 
         'Score', 'Gender', 'Matriculation Year',
       'College', 'Class Of', 'Level', 'Level For Sorting'], 
        'Season', id='flexible_survey_results_color'), lg=2)
           ]),
    dbc.Row([
        dbc.Col(html.H5("College Filter:"), lg=3),
    dbc.Col(
        dcc.Dropdown(df_survey_results_extra_data['College'].unique(),
                 df_survey_results_extra_data['College'].unique(),
                 multi=True,
                id='college_filter'), lg=3),
        ]),
    dbc.Row([
        dbc.Col(html.H5("Level Filter:"), lg=3),
    dbc.Col(dcc.Dropdown(df_survey_results_extra_data['Level'].unique(),
                 df_survey_results_extra_data['Level'].unique(),
                 multi=True,
                id='level_filter'), lg=3)
    ]),
    dcc.Graph(id='flexible_survey_results_view')])

@callback(
    Output('flexible_survey_results_view', 'figure'),
    Input('flexible_survey_results_index', 'value'),
    Input('flexible_survey_results_color', 'value'),
    Input('college_filter', 'value'),
    Input('level_filter', 'value')
)

def display_graph(x_vars, color, college_filter, level_filter):
    print(college_filter,level_filter)

    filter_tuple_list = [
    ('College', 
     college_filter),
    ('Level',level_filter)]
    
    print('x_vars contents and type:',x_vars,type(x_vars))
    print('color contents and type:',color,type(color))
    
    return autopivot_plus_bar(
        df=df_survey_results_extra_data, y='Score', 
        aggfunc='mean', x_vars=x_vars, color=color,
    x_vars_to_exclude=['Level For Sorting'], 
        overall_data_name='All Data',
    weight_col=None, filter_tuple_list=filter_tuple_list)