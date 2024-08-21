# Python for Nonprofits (Version 2)

By Kenneth Burchfiel

Released under the MIT License

In this project, I will demonstrate how nonprofits can use Python to retrieve, analyze, visualize, and share their data. This project is still in its early stages, but I plan to add a number of sections to it as time allows.

*Note*: This project is *not* meant to replace an introductory Python course or textbook. If you're new to Python, I suggest getting started with a resource like [Think Python, 3rd Edition](https://greenteapress.com/wp/think-python-3rd-edition/). (I found the 2nd edition of this book to be very helpful in my own studies.) Once you've finished reading Think Python or have a similar introductory background in the language, you should be in a great position to benefit from this project.

# Contents

Note: many of these sections have not yet been completed or even started; in addition, other sections may be added in later on. I'm working on this project in my free time (which, as a new dad, is not very abundant!), so it may be a while before I begin or finalize a given section.

## Part 1: [Introduction](https://github.com/kburchfiel/pfn_2/tree/main/Introduction)

[The Case for Using Python at Nonprofits](https://github.com/kburchfiel/pfn_2/blob/main/Introduction/the_case_for_python_at_nonprofits.md) explains why you should consider using Python at your nonprofit organization.

## Part 2: Retrieval

### [Data Retrieval](https://github.com/kburchfiel/pfn_2/tree/main/Data_Retrieval)

[data_retrieval.ipynb](https://github.com/kburchfiel/pfn_2/blob/main/Data_Retrieval/data_retrieval.ipynb) (initial draft complete) provides a brief overview of importing data into Python scripts from multiple sources.

### [Data Prep](https://github.com/kburchfiel/pfn_2/tree/main/Data_Prep) 

[data_prep.ipynb](https://github.com/kburchfiel/pfn_2/blob/main/Data_Prep/data_prep.ipynb) (initial draft complete) shows how to clean and reformat data so that it can be incorporated into various analyses.

### [Census Data Imports](https://github.com/kburchfiel/pfn_2/tree/main/Census_Data_Imports)

[census_data_imports.ipynb](https://github.com/kburchfiel/pfn_2/blob/main/Census_Data_Imports/census_data_imports.ipynb) (mostly complete) shows how to use Python to retrieve data from the US Census API, a great source of public-domain demographic data.

## Part 3: Analyses

### [Descriptive Stats](https://github.com/kburchfiel/pfn_2/tree/main/Descriptive_Stats) 

In [descriptive_stats.ipynb](https://github.com/kburchfiel/pfn_2/blob/main/Descriptive_Stats/descriptive_stats.ipynb) (mostly complete), you'll learn how to use Python to calculate a range of descriptive statistics.

### Regression Analyses (not yet started)

This section will show how to create linear regressions within Python. 

## Part 4: Visualizations

### [Graphing](https://github.com/kburchfiel/pfn/tree/main/Graphing) (Work in progress)

Plotly is a powerful tool for creating both interactive and static charts. I've started working on the [graphing.ipynb](https://github.com/kburchfiel/pfn/blob/main/Graphing/graphing.ipynb); once it's complete, it will demonstrate how to create bar, line, and scatter plots along with treemaps (an alternative to pie charts).

### [Mapping](https://github.com/kburchfiel/pfn_2/tree/main/Mapping)

[choropleth_maps.ipynb](https://github.com/kburchfiel/pfn_2/blob/main/Mapping/choropleth_maps.ipynb) (initial draft complete) demonstrates how to use Folium to create interactive choropleth maps. 
Here are examples of the choropleth maps created within this section:

[Net migration rates by county](https://sites.google.com/view/pfn2-choropleth-maps/net-migration-by-county)

[Net migration rates by state](https://sites.google.com/view/pfn2-choropleth-maps/net-migration-by-state?authuser=0)

And here are static copies of these maps:

<img src="https://raw.githubusercontent.com/kburchfiel/pfn_2/main/Mapping/map_screenshots/net_migration_rate_county_2020-2023.png" width="500"/>

<img src="https://raw.githubusercontent.com/kburchfiel/pfn_2/main/Mapping/map_screenshots/net_migration_rate_state_2020-2023.png" width="500"/>

[mapping_census_data.ipynb](https://github.com/kburchfiel/pfn_2/blob/main/Mapping/mapping_census_data.ipynb) (mostly complete) shows how to create maps of the data retrieved via [census_data_imports.ipynb](https://github.com/kburchfiel/pfn_2/blob/main/Census_Data_Imports/census_data_imports.ipynb).


## Part 5: Publication

### Updating Online Spreadsheets (Not yet started)

This section will demonstrate how to use Python to export data to a Google Sheets workbook, thus enabling others to view that data.

### [Online Visualizations](https://github.com/kburchfiel/pfn/tree/main/Online_Visualizations) (Work in progress)

In this section, you'll learn how to use the Dash and Plotly libraries to create interactive online dashboards. The [PFN_Dash_App_Demo](https://github.com/kburchfiel/pfn/tree/main/Online_Visualizations/PFN_Dash_App_Demo) subfolder contains the source code for the main Dash app created within this section; that app [is hosted online here](https://pfndashappdemo-ymc7cs3r5q-uc.a.run.app/). This Dash project provides examples of both simple and more complex dashboards, including ones that make use of the powerful dash-pivottable package.

For a more barebones template that incorporates Flask-Login and Dash pages functionality (and nothing else), visit the [Simple_App_With_Login](https://github.com/kburchfiel/pfn/tree/main/Online_Visualizations/Simple_App_With_Login) section; its corresponding Dash app [can be found here](https://simpleappwithlogin-dsmxn3zfoq-uc.a.run.app/).

## Part 6: [Appendix](https://github.com/kburchfiel/pfn_2/tree/main/Appendix)


I used [nvcu_db_gen.ipynb](https://github.com/kburchfiel/pfn_2/blob/main/Appendix/nvcu_db_gen.ipynb) to construct a SQLite database with **fictional** data for an imaginary university. The tables in this dataset will play a role in many parts of Python for Nonprofits.