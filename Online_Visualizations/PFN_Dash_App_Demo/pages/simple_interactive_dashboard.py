# Simple Enrollment Dashboard
# By Kenneth Burchfiel
# Released under the MIT License

# Parts of this code derive from
# and https://dash.plotly.com/urls 
# and https://dash.plotly.com/minimal-app .

# The Layout page within the Dash Bootstrap Components documentation
# (available at https://dash-bootstrap-components.opensource.faculty.ai/
# docs/components/layout/ )
# provide very helpful in creating this dashboard (along with a number
# of other dashboards within this app.)

import dash
from dash import html, dcc, callback, Output, Input
from data_import import df_curr_enrollment
import plotly.express as px
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/simple_interactive_dashboard')

# Configuring the page's layout:
layout = dbc.Container([
    dbc.Row(dbc.Col(dcc.Markdown('''

    # Simple Interactive Enrollment Dashboard
    
    This dashboard provides a relatively simple overview of NVCU 
    enrollment. There are five preset comparison options and two preset 
    filter options, allowing the user to create a variety of custom views.

    This dashboard is not as versatile or flexible as those that apply the 
    Dash-Pivottable library (e.g. the 'Dash pivottable survey results' 
    dashboard), but it can still serve as a helpful introduction 
    to some of Dash's core features.

    This dashboard also applies the Dash Bootstrap Components (
    https://dash-bootstrap-components.opensource.faculty.ai)
    library in order
    to create a more condensed layout that accommodates a range of 
    screen sizes. This library is also used in certain other dashboards 
    within this app.
    
    '''), lg = 9)),
    dbc.Row([
        dbc.Col(html.H5("Comparison Options:"), lg = 3),
    dbc.Col(dcc.Dropdown(['College', 'Level', 
                  'College and Level', 'Level and College', 
                  'All Students'], 'College and Level', 
                 id = 'simple_enrollment_index'), lg = 2)
           ]),
    dbc.Row([
        dbc.Col(html.H5("College Filter:"), lg = 3),
    dbc.Col(
        dcc.Dropdown(df_curr_enrollment['College'].unique(),
                 df_curr_enrollment['College'].unique(),
                 multi = True,
                id = 'college_filter'), lg = 3),
        ]),
    dbc.Row([
        dbc.Col(html.H5("Level Filter:"), lg = 3),
    dbc.Col(dcc.Dropdown(df_curr_enrollment['Level'].unique(),
                 df_curr_enrollment['Level'].unique(),
                 multi = True,
                id = 'level_filter'), lg = 3)
    ]),
    # For more information about the multi-dropdown option,
    # see https://dash.plotly.com/dash-core-components/dropdown
    dcc.Graph(id='simple_enrollment_view')])

# Configuring a callback that can convert the index and filter options
# specified by the user into a custom chart:

@callback(
    Output('simple_enrollment_view', 'figure'),
    Input('simple_enrollment_index', 'value'),
    Input('college_filter', 'value'),
    Input('level_filter', 'value')
)

# The following function uses the Input values specified above
# to update the chart shown within this page.
def display_graph(pivot_index, college_filter, level_filter):
    
    # Filtering a copy of df_curr_enrollment to include only the filter
    # values specified by the user:
    # print(college_filter, level_filter)
    df_curr_enrollment_for_chart = df_curr_enrollment.copy().query(
        "College in @college_filter & Level in @level_filter")
                                       
    # Using the pivot_index argument to determine which values
    # to pass to the pd.pivot_table() and px.bar() calls within
    # this function:
    if pivot_index == 'College':
        index = 'College'
        x = 'College'
        color = 'College'
        barmode = 'relative'
        
    elif pivot_index == 'Level':
        index = ['Level For Sorting', 'Level']
        x = 'Level'
        color = 'Level'
        barmode = 'relative'
        
    elif pivot_index == 'College and Level':
        index = ['College', 'Level For Sorting', 'Level']
        x = 'College'
        color = 'Level'
        barmode = 'group'
        
    elif pivot_index == 'Level and College':
        index = ['Level For Sorting', 'Level', 'College']
        x = 'Level'
        color = 'College'
        barmode = 'group'
        
    elif pivot_index == 'All Students': # In this case, all data will
        # be grouped together. We'll create a new column named
        # 'All Students' that can serve as the x axis label for this data.
        df_curr_enrollment_for_chart['All Students'] = 'All Students'
        index = 'All Students'
        color = 'All Students'
        x = 'All Students'
        barmode = 'relative'
        
    # Creating a pivot table that can serve as the basis for our 
    # enrollment chart:
    df_simple_enrollment_pivot = df_curr_enrollment_for_chart.pivot_table(
    index = index,
    values = 'Enrollment', aggfunc = 'sum').reset_index()
    
    # Creating this chart:
    fig_simple_enrollment = px.bar(df_simple_enrollment_pivot, 
       x = x, y = 'Enrollment', color = color,
      text_auto = '.0f', barmode = barmode,
      title = f'NVCU Enrollment by {pivot_index}')
    return fig_simple_enrollment
    

