## Interactive Dashboard App with Dash-Pivottable and Flask-Login Functionality

[Click here](https://pfndashappdemo-ymc7cs3r5q-uc.a.run.app/) to view the Google Cloud Run-hosted version of this app. (If no one has accessed the app recently, it will take several seconds to load--as the app is set to run on demand in order to save costs.)

This project demonstrates how to use Dash to create interactive online visualizations. These visualizations range from simple charts to more complex interactive setups.

The [simple_enrollment_dashboard](https://pfndashappdemo-ymc7cs3r5q-uc.a.run.app/simple_enrollment_dashboard) page displays a relatively basic interactive enrollment dashboard. This dashboard didn't take much code at all to write, but its functionality is rather limited.

For more advanced and versatile dashboards, visit the [dash_pivottable_enrollment](https://pfndashappdemo-ymc7cs3r5q-uc.a.run.app/dash_pivottable_enrollment) and [dash_pivottable_survey_results](https://pfndashappdemo-ymc7cs3r5q-uc.a.run.app/dash_pivottable_survey_results) pages. Both of these dashboards make use of the powerful dash-pivottable library.

## Development notes:

1. I made use of a standalone Jupyter notebook (notebook_for_testing.ipynb) to test out code before integrating it into my Dash app files.

1. The source data is imported from GitHub. A more realistic approach would retrieve data from an online database; however, that would cause this project to incur a monthly database hosting expense.