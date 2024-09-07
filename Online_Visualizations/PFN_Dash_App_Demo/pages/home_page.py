# This code derives from 
# and https://dash.plotly.com/urls .

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/')

layout = dbc.Container([
    dcc.Markdown(''' 
    # [Python For Nonprofits](https://github.com/kburchfiel/pfn)' \
    Main Dash App Demo \
    
    This project demonstrates how to use Dash to create \
    interactive online visualizations. These visualizations range \
    from simple charts to more complex interactive setups.

    The **/simple_interactive_dashboard** page displays a relatively \
    straightforward interactive enrollment dashboard. This dashboard \
    didn't require much code to write, but its functionality is rather \ 
    limited.

    The **/fixed_dashboard** page shows an even simpler dashboard that \ 
    lacks user-defined filter and comparison settings. 
    
    The **/flexible_survey_results_dashboard** and \
    **/flexible_enrollment_dashboard** pages allow for a wide range of 
    comparison and color options. These options are made possible by the 
    autopivot() and autobar() functions found within \
    auto_pivot_and_graph.py (see source code for details). The 
    flexible_enrollment_dashboard also makes use of an import_layout() 
    function in order to reduce the amount of code needed to define
    the page's structure and menu options.

    The dash-pivottable library makes it very easy to \
    create interactive dashboards. Examples of this library in use can \
    be found within the **/dash_pivottable_enrollment** \
    and **/dash_pivottable_survey_results** pages.'''
    )])