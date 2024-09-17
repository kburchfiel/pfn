## Interactive Dashboard App with Dash-Pivottable and Flask-Login Functionality

**[Click here](https://pfndashappdemo-ymc7cs3r5q-uc.a.run.app/) to view the Google Cloud Run-hosted version of this app.** *(If no one has accessed the app recently, it will take several seconds to load, as the app is set to run on demand in order to save costs.)*

This project demonstrates how to use Dash to create 
interactive online visualizations. These visualizations range 
from simple charts to more complex interactive setups.

The [Fixed Dashboard](https://pfndashappdemo-ymc7cs3r5q-uc.a.run.app/fixed_dashboard) page shows a very simple 
dashboard setup that lacks user-defined filter and comparison settings. 

<img src="https://raw.githubusercontent.com/kburchfiel/pfn/main/Online_Visualizations/PFN_Dash_App_Demo/page_screenshots/fixed_dashboard.png" width="300"/>

The [Simple Interactive Dashboard](https://pfndashappdemo-ymc7cs3r5q-uc.a.run.app/simple_interactive_dashboard) page 
displays a relatively straightforward interactive enrollment dashboard. 
This dashboard didn't require much code to write, but its functionality 
is rather limited.

<img src="https://raw.githubusercontent.com/kburchfiel/pfn/main/Online_Visualizations/PFN_Dash_App_Demo/page_screenshots/simple_interactive_enrollment_dashboard.png" width="400"/>


The [Flexible Survey Results](https://pfndashappdemo-ymc7cs3r5q-uc.a.run.app/flexible_survey_results_dashboard) and 
[Flexible Enrollment](https://pfndashappdemo-ymc7cs3r5q-uc.a.run.app/flexible_enrollment_dashboard) dashboard pages
allow for a wide range of comparison and color options. These options are 
made possible by the autopivot() and autobar() functions found within 
[auto_pivot_and_graph.py](https://github.com/kburchfiel/pfn/blob/main/Online_Visualizations/PFN_Dash_App_Demo/auto_pivot_and_graph.py). (You may also find these functions useful for 
developing standlone Plotly charts.)

The Flexible Enrollment Dashboard also makes use of an import_layout() 
function (stored within [import_layout.py](https://github.com/kburchfiel/pfn/blob/main/Online_Visualizations/PFN_Dash_App_Demo/import_layout.py)) 
in order to reduce the amount of code needed to define
the page's structure and menu options. In addition, this dashboard
applies the autotable() function in [auto_pivot_and_graph.py](https://github.com/kburchfiel/pfn/blob/main/Online_Visualizations/PFN_Dash_App_Demo/auto_pivot_and_graph.py)) to display
a tabular view of the data featured in the graph.

<img src="https://raw.githubusercontent.com/kburchfiel/pfn/main/Online_Visualizations/PFN_Dash_App_Demo/page_screenshots/flexible_enrollment_dashboard.png" width="400"/>

The dash-pivottable library makes it very easy to 
create interactive dashboards. Examples of this library in use can 
be found within the [Dash Pivottable (Enrollment)](https://pfndashappdemo-ymc7cs3r5q-uc.a.run.app/dash_pivottable_enrollment) and [Dash Pivottable (Survey Results)](https://pfndashappdemo-ymc7cs3r5q-uc.a.run.app/dash_pivottable_survey_results) pages.

<img src="https://raw.githubusercontent.com/kburchfiel/pfn/main/Online_Visualizations/PFN_Dash_App_Demo/page_screenshots/dash_pivottable_enrollment.png" width="600"/>


## Development notes:

1. I made use of a standalone Jupyter notebook ([notebook_for_testing.ipynb](https://github.com/kburchfiel/pfn/blob/main/Online_Visualizations/PFN_Dash_App_Demo/notebook_for_testing.ipynb)) to test out code before integrating it into my Dash app files.

1. The source data is imported from GitHub. A more realistic approach would retrieve data from an online database; however, that would cause this project to incur a monthly database hosting expense.

1. The [dash-bootstrap-components](https://dash-bootstrap-components.opensource.faculty.ai/docs/components/layout/) library is used extensively within many of these dashboards. It's a great option for making your dashboards more aesthetically pleasing *and* more flexible.

1. This app is hosted on Google Cloud Run, though you can also host it locally by cloning this project. See the [Simple App With Login](https://github.com/kburchfiel/pfn/tree/main/Online_Visualizations/Simple_App_With_Login) Readme for more guidance on hosting Dash apps within Cloud Run.