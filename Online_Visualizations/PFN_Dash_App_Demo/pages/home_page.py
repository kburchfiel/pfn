# This code derives from 
# and https://dash.plotly.com/urls .

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/')

layout = dbc.Container([
    dcc.Markdown(''' 
## [Python For Nonprofits](https://github.com/kburchfiel/pfn)' \
Main Dash App Demo 

This project demonstrates how to use Dash to create 
interactive online visualizations. These visualizations range 
from simple charts to more complex interactive setups.

The [Fixed Dashboard](/fixed_dashboard) page shows a very simple 
dashboard setup that lacks user-defined filter and comparison settings. 

The [Simple Interactive Dashboard](/simple_interactive_dashboard) page 
displays a relatively straightforward interactive enrollment dashboard. 
This dashboard didn't require much code to write, but its functionality 
is rather limited.

The [Flexible Survey Results](/flexible_survey_results_dashboard) and 
[Flexible Enrollment](/flexible_enrollment_dashboard) dashboard pages
allow for a wide range of comparison and color options. These options are 
made possible by the autopivot() and autobar() functions found within 
[auto_pivot_and_graph.py](https://github.com/kburchfiel/pfn/blob/main/\
Online_Visualizations/PFN_Dash_App_Demo/auto_pivot_and_graph.py). (You may
also find these functions useful for developing standlone Plotly charts.)

The Flexible Enrollment Dashboard also makes use of an import_layout() 
function (stored within [import_layout.py](https://github.com/\
kburchfiel/pfn/blob/main/Online_Visualizations/
PFN_Dash_App_Demo/import_layout.py)) 
in order to reduce the amount of code needed to define
the page's structure and menu options. In addition, this dashboard
applies the autotable() function in [auto_pivot_and_graph.py](https://\
github.com/kburchfiel/pfn/blob/main/Online_Visualizations/\
PFN_Dash_App_Demo/auto_pivot_and_graph.py)) to display
a tabular view of the data featured in the graph.

The dash-pivottable library makes it very easy to 
create interactive dashboards. Examples of this library in use can 
be found within the [Dash Pivottable (Enrollment)]\
(/dash_pivottable_enrollment) and [Dash Pivottable (Survey Results)]\
(/dash_pivottable_survey_results) pages.

The source code for these dashboards can be found [at this link](https://\
github.com/kburchfiel/pfn/tree/main/\
Online_Visualizations/PFN_Dash_App_Demo).

'''
    )])