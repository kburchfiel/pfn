# Flexible survey_results Dashboard
# By Kenneth Burchfiel
# Released under the MIT License

# Parts of this code derive from
# and https://dash.plotly.com/urls 
# and https://dash.plotly.com/minimal-app .


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
    results. It utilizes the autopivot() and autobar() functions found within
    auto_pivot_and_graph.py to allow for a wide range of display options.
    
    '''), lg = 9)),
    dbc.Row([
        dbc.Col(html.H5("Comparison Options:"), lg = 3),
    dbc.Col(dcc.Dropdown(
        ['Starting Year', 'Season', 'Gender', 'Matriculation Year',
       'College', 'Class Of', 'Level', 'Level For Sorting'], 
        ['College', 'Season'], multi = True,
                 id = 'flexible_survey_results_index'), lg = 3),
        dbc.Col(html.H5("Color Option:"), lg = 2),
    dbc.Col(dcc.Dropdown(
        ['Starting Year', 'Season', 
         'Score', 'Gender', 'Matriculation Year',
       'College', 'Class Of', 'Level', 'Level For Sorting'], 
        'Season', id = 'flexible_survey_results_color'), lg = 2)
           ]),
    dbc.Row([
        dbc.Col(html.H5("College Filter:"), lg = 3),
    dbc.Col(
        dcc.Dropdown(df_survey_results_extra_data['College'].unique(),
                 df_survey_results_extra_data['College'].unique(),
                 multi = True,
                id = 'college_filter'), lg = 3),
        ]),
    dbc.Row([
        dbc.Col(html.H5("Level Filter:"), lg = 3),
    dbc.Col(dcc.Dropdown(df_survey_results_extra_data['Level'].unique(),
                 df_survey_results_extra_data['Level'].unique(),
                 multi = True,
                id = 'level_filter'), lg = 3)
    ]),
    # For more information about the multi-dropdown option,
    # see https://dash.plotly.com/dash-core-components/dropdown
    dcc.Graph(id='flexible_survey_results_view')])

# Configuring a callback that can convert the index and filter options
# specified by the user into a custom chart:

@callback(
    Output('flexible_survey_results_view', 'figure'),
    Input('flexible_survey_results_index', 'value'),
    Input('flexible_survey_results_color', 'value'),
    Input('college_filter', 'value'),
    Input('level_filter', 'value')
)

# The following function calls autopivot_plus_bar to convert
# the input values specified above into a bar chart:
def display_graph(x_vars, color, college_filter, level_filter):
    print(college_filter,level_filter)

    # Creating a list of tuples that can be used to filter
    # the output:
    filter_tuple_list = [
    ('College', 
     college_filter),
    ('Level',level_filter)]
    
    print('x_vars contents and type:',x_vars,type(x_vars))
    print('color contents and type:',color,type(color))
    
    return autopivot_plus_bar(
        df = df_survey_results_extra_data, y = 'Score', 
        aggfunc = 'mean', x_vars = x_vars, color = color,
    x_vars_to_exclude = ['Level For Sorting'], 
        overall_data_name = 'All Data',
    weight_col = None, filter_tuple_list = filter_tuple_list)