# This code derives from 
# and https://dash.plotly.com/urls .

import dash
from dash import html

dash.register_page(__name__, path='/')

layout = html.Div([
    html.H1('Pivot Table Examples'),
    html.Div('This project demonstrates how to apply the \
powerful dash-pivottable library to easily create interactive dashboards.'),
html.Div('The enrollment and survey results dashboards can be accessed via \
/enrollment_pivot and /survey_results_pivot, respectively.')])