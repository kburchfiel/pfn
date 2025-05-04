# Flexible Enrollment Dashboard
# By Kenneth Burchfiel
# Released under the MIT License

# Parts of this code derive from
# and https://dash.plotly.com/urls 
# and https://dash.plotly.com/minimal-app .

import dash
from dash import html, dcc, callback, Output, Input, dash_table
import dash_bootstrap_components as dbc

from data_import import df_curr_enrollment
import plotly.express as px

# The following auto_pivot_and_graph code was featured 
# within the Pivot and Graph Functions section of PFN.

from auto_pivot_and_graph import autopivot_plus_bar
from import_layout import import_layout

dash.register_page(__name__, path='/flexible_enrollment_dashboard')

# Determining which comparison and color options to pass to
# the import_layout() function that will define part of the 
# dashboard's layout:

# These lists of options will get initialized as all columns within
# the DataFrame *except* for those present in cols_to_exclude. (If there
# are many columns within the DataFrame, this approach can require
# less typing than would adding in all columns to be included.)

cols_to_exclude = [
    'Date Of Birth', 'First Name', 'Last Name', 
    'Student ID', 'Matriculation Number', 'Enrollment']
comparison_list = list(
    set(df_curr_enrollment.columns) - set(cols_to_exclude))
# Converting a list of items into a set can make it easier to remove
# a group of items from that set. For more on this data type, see
# https://docs.python.org/3/tutorial/datastructures.html#sets .

color_list = comparison_list.copy() # These lists can contain
# the same values.

# Setting default comparison and color values:
comparison_default = ['Level For Sorting', 'Level']
color_default = 'College'

filter_cols = ['College', 'Level', 'Gender']
# Note that each of these values must be added to
# the @callback() component of this page along with
# the display_graph inputs.
# (Add '_filter' after each column name within the Callback section.
# For instance, 'College' will map to 'College_filter.') 

# Configuring the page's layout:
# The import_layout() function will make it easier to create the
# central part of the page's layout.
# (Note the use of + to combine different lists of layout components
# together.)

layout = dbc.Container([
    dbc.Row(dbc.Col(dcc.Markdown('''

    # Flexible Interactive Enrollment Dashboard
    
    This dashboard provides a flexible overview of NVCU enrollment. 
    It utilizes the autopivot(), autobar(), and autotable() functions 
    found within auto_pivot_and_graph.py to allow for a wide range 
    of display options. It also uses the import_layout() function 
    found in import_layout.py to define a sizeable component 
    of the page's layout.
    
    '''), lg = 9))] +
    import_layout(df=df_curr_enrollment, 
                  comparison_list=comparison_list,
                 comparison_default=comparison_default,
                 color_list=color_list,
                 color_default=color_default, 
                  filter_cols=filter_cols) +
    # For more information about the multi-dropdown option,
    # see https://dash.plotly.com/dash-core-components/dropdown . 
    [dcc.Graph(id='flexible_enrollment_graph')] + 
    [dcc.Graph(id='flexible_enrollment_table')]
) 

# Configuring a callback that can convert the index and filter options
# specified by the user into a custom chart:

@callback(
    Output('flexible_enrollment_graph', 'figure'),
    Output('flexible_enrollment_table', 'figure'),
    Input('comparison_options', 'value'),
    Input('color_option', 'value'),
    Input('College_filter', 'value'),
    Input('Level_filter', 'value'),
    Input('Gender_filter', 'value')
)

# The following function calls autopivot_plus_bar() to convert
# the input values specified above into a bar chart:
def display_graph(x_vars, color, college_filter, 
                  level_filter, gender_filter):
    print(college_filter,level_filter, gender_filter)

    # Creating a list of tuples that can be used to filter
    # the output:
    filter_tuple_list = [
    ('College', 
     college_filter),
    ('Level',level_filter),
    ('Gender',gender_filter)
    ]
    print('x_vars contents and type:',x_vars,type(x_vars))
    print('color contents and type:',color,type(color))

    # '' is passed to custom_aggfunc_name so that
    # the chart title will begin with 'Enrollment'
    # rather than 'Total Enrollment.'
    bar_graph, table = autopivot_plus_bar(
        df=df_curr_enrollment, y='Enrollment', 
        aggfunc='sum', x_vars=x_vars, color=color,
    x_vars_to_exclude=['Level For Sorting'], 
        overall_data_name='All Data',
    weight_col=None, filter_tuple_list=filter_tuple_list,
    custom_aggfunc_name='', create_table=True,
    text_auto='.0f')

    print(table)

    return bar_graph, table