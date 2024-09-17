# import_layout() function definition
# By Kenneth Burchfiel
# Released under the MIT license

import dash
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

def import_layout(df, comparison_list, comparison_default, 
                 color_list, color_default, filter_cols = []):
    '''This function generates comparison, color, and filter
    components of an interactive dashboard, thus reducing
    the amount of code needed to create a multi-dashboard Dash app
    and helping ensure consistency across dashboard layouts.

    df: the DataFrame from which filter options should be retrieved.
    
    comparison_list and color_list: a list of comparison and color
    options to pass to the Comparison Options and Color Option menus,
    respectively.
    
    comparison_default and color_default: the default comparison
    and color options for comparison_list and color_list, respectively.

    filter_cols: The columns in df for which to create filter dropdowns.
    '''

    df_layout = df.copy() # This step ensures that this function
    # will not make any changes to df.

    # Initializing the layout that will be returned to
    # the Dash app code:
    # This layout will include rows for comparisons and color options.
    layout = [dbc.Row([
        dbc.Col(html.H5("Comparison Options:"), lg = 2),
    dbc.Col(dcc.Dropdown(
        comparison_list,
        comparison_default, multi = True,
                 id = 'comparison_options'), lg = 3),
        dbc.Col(html.H5("Color Option:"), lg = 2),
    dbc.Col(dcc.Dropdown(
        color_list, color_default, 
        id = 'color_option'), lg = 2)])]

    # Adding filter rows for each column in filter_cols:
    # Note that each filter will get added to the layout
    # via an addition operation.
    for filter_col in filter_cols:
        layout += [dbc.Row([
        dbc.Col(html.H5(f"{filter_col} Filter:"), lg = 2),
        dbc.Col(
        dcc.Dropdown(df_layout[filter_col].unique(),
                 df_layout[filter_col].unique(),
                 multi = True,
                id = f'{filter_col}_filter'), lg = 3)
        ])]

    # print("Layout:",layout) # May be useful for debugging

    
    return layout