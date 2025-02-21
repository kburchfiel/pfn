# PFN Dash App Demo

## Readme

**Visit https://pfndashappdemo-ymc7cs3r5q-uc.a.run.app/ to view the Google Cloud Run-hosted version of this app.** *(If no one has accessed the app recently, it will take several seconds to load, as the app is set to run on demand in order to save costs.)*

This project demonstrates how to use Dash to create interactive online visualizations. These visualizations range from simple charts to more complex interactive setups. Both the Flask-Login and Dash-Pivottable libraries are featured within this project.

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


### Development notes:

1. I made use of a standalone Jupyter notebook ([notebook_for_testing.ipynb](https://github.com/kburchfiel/pfn/blob/main/Online_Visualizations/PFN_Dash_App_Demo/notebook_for_testing.ipynb)) to test out code before integrating it into my Dash app files.

1. The source data is imported from GitHub. A more realistic approach would retrieve data from an online database; however, that would cause this project to incur a monthly database hosting expense.

1. The [dash-bootstrap-components](https://dash-bootstrap-components.opensource.faculty.ai/docs/components/layout/) library is used extensively within many of these dashboards. It's a great option for making your dashboards more aesthetically pleasing *and* more flexible.

1. This app is hosted on Google Cloud Run, though you can also host it locally by cloning this project. See the 'Development and setup notes' section below for more guidance on hosting Dash apps within Cloud Run.

### Project structure

The files and folders in this app are arranged as follows: 

(Folders have '/' suffixes. Note that Procfile is an 'extensionless' document rather than a folder.)

pages/

----home_page.py

----fixed_dashboard.py

----simple_interactive_dashboard.py

----flexible_survey_results_dashboard.py

----flexible_enrollment_dashboard.py

----dash_pivottable_enrollment.py

----dash_pivottable_survey_results.py

templates/

----login.html

app.py

auto_pivot_and_graph.py

data_import.py

import_layout.py

Procfile

readme.md [this file]

requirements.txt

### Development and setup notes

Some of the code in this folder was derived from jinnyzor's post at https://community.plotly.com/t/dash-app-pages-with-flask-login-flow-using-flask/69507/38 . Jinnyzor [wrote regarding that post](https://community.plotly.com/t/dash-app-pages-with-flask-login-flow-using-flask/69507/55): "this is free to use, no license." I am very grateful to jinnyzor (and to [Nader Elshehabi](https://github.com/naderelshehabi/dash-flask-login)) for allowing us to use their code!

Some code also derives from that found in the [Dash Pages documentation](https://dash.plotly.com/urls).

#### Steps for hosting this Dash app (with Flask-Login functionality) on Google Cloud Run

<h2 style="color:red">Warning: These steps may cause you to incur hosting charges depending on how frequently your site is visited. I recommend setting billing alerts to keep track of your spending.</h2>

Heroku, an alternative site for hosting Dash apps, offers maximum monthly spending caps, which could help you control your costs; however, it's possible that the minimum amount you would pay on Herkou would be higher than your minimum on Cloud Run. (This is why I chose to deploy this app to Cloud Run rather than Heroku.) Heroku pricing information [can be found here](https://www.heroku.com/pricing).</h2>

1. Visit https://console.cloud.google.com/. (Create a Google Cloud Console account if needed).

2. Create a new project. I named mine 'pyfono' (short for 'Python for Nonprofits'--I couldn't use 'pfn' because it needed to be at least 4 characters long).

3. Follow [the steps outlined here](https://cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-python-service)--but note the modifications that I've made to these steps below.

5. If you need to install the Google Cloud Command Line Interface (CLI), you can do so [on this page](https://cloud.google.com/sdk/docs/install). I deselected the 'Bundled Python' component during the installation process since (not surprisingly) I already had Python present on my computer.

I also used the following contents in place of the recommended requirements.txt values:
Flask
gunicorn
Werkzeug
dash
Flask-Login
dash-pivottable
pandas
dash-bootstrap-components

(These libraries will be imported from pip. Therefore, in order to determine what format of their name to use, visit the library on Pypi and then enter the text following the 'pip install' example. For instance, on the [Flask-Login](https://pypi.org/project/Flask-Login/) page, you'll see 'pip install Flask Login'; therefore, add Flask-Login to the requirements.txt page rather than flask-login (its name within conda) or flask_login (its name within app.py).

(Also note that entering `gcloud run deploy --source .` (don't forget the space and period!) rather than `gcloud run deploy` saves you a step during the deployment process.)

The [Google Cloud Region Picker](https://cloud.withgoogle.com/region-picker/) site can help you determine where to host your app. (When prompted for my region choice, I entered 32 for us-central1.

4. You'll also want to add a file named Procfile (no extension) with the following text:
web: gunicorn app:server

(This line came from https://dash.plotly.com/deployment)

I was prompted to enter this line after seeing the following error message within my Google Cloud Console log:

`Step #1: [builder] failed to build: for Python, provide a main.py file or set an entrypoint with "GOOGLE_ENTRYPOINT" env var or by creating a "Procfile" file"`

5. Hopefully, after Google Cloud finishes processing your deployment request, you'll see a message like the following:

`Service [dashappdemo] revision [dashappdemo-00002-xdj] has been deployed and is serving 100 percent of traffic.
Service URL: https://pfndashappdemo-ymc7cs3r5q-uc.a.run.app/`

To confirm that your page is operating correctly, visit its service URL (e.g. https://pfndashappdemo-ymc7cs3r5q-uc.a.run.app/, in the case of this app). Ideally, you'll see the same screen that you would when deploying the app locally. 

If you instead see 'Service Unavailable', don't panic! There's something about your deployment that isn't quite correct. Perhaps you forgot to include a library within requirements.txt that your script uses, for instance. Make sure to check your logs (available at https://console.cloud.google.com/logs/) for clues as to what might be going wrong with your script.

(For example, seeing "ModuleNotFoundError: No module named 'pandas'" within my log after one failed deployment made me realize that I had forgotten to add pandas to my requirements.txt file.)

If you receive a message like "service account 13371337-compute@developer.gserviceaccount.com does not have access to the bucket," try entering `gcloud auth login` and redoing the login procedure (as suggested by StackOverflow user Lee here: https://stackoverflow.com/a/70377891/13097194 ).

6. After deploying a new version of your app, you may want to delete the old version (especially if it failed to run to begin with) in order to save costs. You can do so by searching for 'Artifact Registry' within the Cloud Console website; navigating to the list of containers for your site; and then keeping only the most recent container. Likewise, you may want to keep only the most recent bucket within the source/ folder in your Cloud Storage bucket. (To delete the other ones, search for 'buckets' within your Cloud Console; click on your bucket name; click on the 'source/' folder; and then delete all but the most recent bucket.)

