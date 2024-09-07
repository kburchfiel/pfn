## Interactive Dashboard App with Dash-Pivottable and Flask-Login Functionality

[Click here](https://pfndashappdemo-ymc7cs3r5q-uc.a.run.app/) to view the Google Cloud Run-hosted version of this app. (If no one has accessed the app recently, it will take several seconds to load--as the app is set to run on demand in order to save costs.)

This project demonstrates how to use Dash to create interactive online visualizations. These visualizations range from simple charts to more complex interactive setups.

The [simple_interactive_dashboard](https://pfndashappdemo-ymc7cs3r5q-uc.a.run.app/simple_interactive_dashboard) page displays a relatively basic interactive enrollment dashboard. This dashboard didn't take much code at all to write, but its functionality is rather limited.

An even simpler enrollment dashboard that foregoes the the comparison and filter options present within the simple_interactive_dashboard page can be found at [fixed_dashboard](https://pfndashappdemo-ymc7cs3r5q-uc.a.run.app/fixed_dashboard). The 'static' approach used within this dashboard has significant limitations, but it may still be helpful as a reference.

The [flexible_survey_results_dashboard](https://pfndashappdemo-470317599391.us-central1.run.app/flexible_survey_results_dashboard) page shows a more complex dashboard that utilizes the autopivot() and autobar() functions in [auto_pivot_and_graph.py](https://github.com/kburchfiel/pfn/blob/main/Online_Visualizations/PFN_Dash_App_Demo/auto_pivot_and_graph.py). These two functions allow for a wide range of comparison and color options.

The [flexible_enrollment_dashboard](https://pfndashappdemo-470317599391.us-central1.run.app/flexible_enrollment_dashboard) page has a similar setup to that of the flexible survey results dashboard except that it also utilizes the import_layout() function found in [import_layout.py](https://github.com/kburchfiel/pfn/blob/main/Online_Visualizations/PFN_Dash_App_Demo/import_layout.py). This function can simplify the process of building Dash app pages' layouts.


The [dash-pivottable library](https://github.com/plotly/dash-pivottable) greatly simplifies the process of creating complex interactive dashboards. This library, along with its [usage.py example code](https://github.com/plotly/dash-pivottable/blob/master/usage.py), powers the  [dash_pivottable_enrollment](https://pfndashappdemo-ymc7cs3r5q-uc.a.run.app/dash_pivottable_enrollment) and [dash_pivottable_survey_results](https://pfndashappdemo-ymc7cs3r5q-uc.a.run.app/dash_pivottable_survey_results) pages.

## Development notes:

1. I made use of a standalone Jupyter notebook ([notebook_for_testing.ipynb](https://github.com/kburchfiel/pfn/blob/main/Online_Visualizations/PFN_Dash_App_Demo/notebook_for_testing.ipynb)) to test out code before integrating it into my Dash app files.

1. The source data is imported from GitHub. A more realistic approach would retrieve data from an online database; however, that would cause this project to incur a monthly database hosting expense.

1. The [dash-bootstrap-components](https://dash-bootstrap-components.opensource.faculty.ai/docs/components/layout/) library is used extensively within many of these dashboards. It's a great option for making your dashboards more aesthetically pleasing *and* more flexible.

1. See the [Simple App With Login](https://github.com/kburchfiel/pfn/tree/main/Online_Visualizations/Simple_App_With_Login) Readme for more guidance on hosting Dash apps within Cloud Run.