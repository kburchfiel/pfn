# This code derives from 
# and https://dash.plotly.com/urls .

import dash
from dash import html, dcc

dash.register_page(__name__, path='/')

layout = html.Div([
    dcc.Markdown(''' 
    # [Python For Nonprofits](https://github.com/kburchfiel/pfn)' \
    Main Dash App Demo \
    
    This project demonstrates how to use Dash to create \
    interactive online visualizations. These visualizations range \
    from simple charts to more complex interactive setups.

    The **/simple_enrollment_dashboard** page displays a relatively straightforward
    interactive enrollment dashboard. This dashboard didn't take much
    code at all to write, but its functionality is rather limited.
    
    The dash-pivottable library makes it very easy to \
    create interactive dashboards. Examples of this library in use can \
    be found within the **/dash_pivottable_enrollment** \
    and **/dash_pivottable_survey_results** pages.'''
    )])