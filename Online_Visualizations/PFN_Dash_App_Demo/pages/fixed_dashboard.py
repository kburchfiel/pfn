# Sample Fixed Dashboard
# By Kenneth Burchfiel
# Released under the MIT License

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from data_import import df_curr_enrollment
import plotly.express as px

# Creating a pivot table that can serve as the basis of our enrollment
# by college and level graph:

df_enrollment_by_college_and_level = df_curr_enrollment.pivot_table(
    index=['College', 'Level For Sorting', 'Level'],
    values='Enrollment', aggfunc='sum').reset_index()

# Creating a graph of this pivot table:
fig_enrollment_by_college_and_level = px.bar(
    df_enrollment_by_college_and_level, 
       x='College', y='Enrollment', color='Level',
      barmode='group',
      text_auto='.0f',
      title='NVCU Enrollment by College and Level')

# Performing the same steps for simpler charts that show enrollment
# by college and by level (but not both):
df_enrollment_by_college = df_curr_enrollment.pivot_table(
    index=['College'],
    values='Enrollment', aggfunc='sum').reset_index()

fig_enrollment_by_college = px.bar(df_enrollment_by_college, 
    x='College', y='Enrollment', color='College',
    text_auto='.0f',
    title='NVCU Enrollment by College')

df_enrollment_by_level = df_curr_enrollment.pivot_table(
    index=['Level For Sorting', 'Level'],
    values='Enrollment', aggfunc='sum').reset_index()

fig_enrollment_by_level = px.bar(df_enrollment_by_level, 
       x='Level', y='Enrollment', color='Level',
      text_auto='.0f',
      title='NVCU Enrollment by Level')

dash.register_page(__name__, path='/fixed_dashboard')

layout = dbc.Container([
    dcc.Markdown(''' # Simple Fixed Dashboard

    This dashboard contains three bar charts that display enrollment 
    totals by college and level; college; and level. Plotly's built-in 
    tools make these charts somewhat interactive; however, no additional  
    comparison or filter options are provided. The other dashboards
    within this app allow for more user interaction.
    
    '''),
    dcc.Graph(figure=fig_enrollment_by_college_and_level),
    # This method of hosting a fixed graph within a Dash page (without any
    # callbacks) came from https://dash.plotly.com/
    # tutorial#visualizing-data .
    dcc.Graph(figure=fig_enrollment_by_college),
    dcc.Graph(figure=fig_enrollment_by_level)
])