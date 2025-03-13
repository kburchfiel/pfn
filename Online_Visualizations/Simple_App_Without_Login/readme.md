# Simple Dash App Without Login

## Introduction to the Online Visualizations section of Python for Nonprofits

PFN's Online Visualizations section will demonstrate how to host visualizations online via Dash, a powerful Python library made by the same team that develops Plotly.

Two separate Dash apps will be featured in this section:

1. A simple Dash app that doesn't require users to log in.

2. PFN Dash App Demo, a more detailed Dash app that shows dashboards of varying complexity and also requires users to log in.

These apps take the form of a series of files, most of which (but not all) are .py scripts. In order to get them to run successfully on your own computer, it's very important to (1) consult their corresponding documentation closely and (2) use the same folder structure that is shown within the Python for Nonprofits GitHub page.

It's *also* important to note that **you may incur some costs when deploying Dash apps online via Google Cloud Run** (the method shown within these notebooks). I have found the costs to be quite small on my end (literally pennies a month), but more complex and widely accessed apps will of course incur higher costs. If you want to avoid these costs, you can simply run these apps locally on your own machine. 


## The 'Simple App Without Login' project itself

### Readme

(Note: the Cloud Run-hosted version of this app can be found at https://simpleappwithoutlogin-470317599391.us-central1.run.app/ .)

This folder provides sample code for a Dash app that can be deployed to Cloud Run. This code was based on the app deployment steps found in https://dash.plotly.com/deployment and https://cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-python-service . (The Plotly walkthrough shows how to deploy a Dash app to Heroku, and the Cloud Run walkthrough shows how to deploy a Flask App to Cloud Run; by taking bits from each, you can then learn how to deploy a *Dash* app to *Cloud Run.* :)

#### Development and setup notes

1. The dash-bootstrap-components (https://dash-bootstrap-components.opensource.faculty.ai/docs/components/layout/) library is used extensively within many of these dashboards. It's a great option for making your dashboards more aesthetically pleasing *and* more flexible.

1. This app is hosted on Google Cloud Run, though you can also host it locally by cloning this project. See the following section for more guidance on hosting Dash apps within Cloud Run.


#### Rationale for hosting this Dash app on Google Cloud Run

Heroku, an alternative site for hosting Dash apps, offers maximum monthly spending caps, which could help you control your costs; however, it's possible that the minimum amount you would pay on Herkou would be higher than your minimum on Cloud Run. (This is why I chose to deploy this app to Cloud Run rather than Heroku.) Heroku pricing information can be found at https://www.heroku.com/pricing .</h2>

#### Steps for deploying this app to Cloud Run

(Some of these steps will apply to many different Cloud Run-hosted Dash apps; however, in order to replicate this online app on your end, you'll also need to review the following section, which explains how to connect your Dash app to Google Sheets.)

<h2 style="color:red">Warning: These steps may cause you to incur hosting charges depending on how frequently your site is visited. I recommend setting billing alerts to keep track of your spending.</h2>

1. Visit https://console.cloud.google.com/ . (Create a Google Cloud Console account if needed).

2. Create a new project. (Note that you *can* deploy multiple Dash apps within the same project if needed.

3. Follow the steps outlined here (https://cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-python-service)--but note the modifications that I've made to these steps below.

5. If you need to install the Google Cloud Command Line Interface (CLI), you can do so at (https://cloud.google.com/sdk/docs/install. I deselected the 'Bundled Python' component during the installation process since (not surprisingly) I already had Python present on my computer.

I also used the following contents in place of the recommended requirements.txt values:

```
gspread
gspread-dataframe
dash
plotly
pandas
gunicorn
dash-bootstrap-components
```

(These libraries will be imported from pip. Therefore, in order to determine what format of their name to use, visit the library on Pypi and then enter the text following the 'pip install' example. For instance, on the gspread-dataframe PyPI page (https://pypi.org/project/gspread-dataframe/), you'll see `pip install gspread-dataframe` as the recommended installation command; therefore, add `gspread-dataframe` to the requirements.txt page rather than `gspread-dataframe` (its name within conda) or `gspread_dataframe` (its name within `app.py`).

(Also note that entering `gcloud run deploy --source .` (don't forget the space and period!) rather than `gcloud run deploy` saves you a step during the deployment process.)

The Google Cloud Region Picker (https://cloud.withgoogle.com/region-picker/) site can help you determine where to host your app. (When prompted for my region choice, I entered `us-central1`. Note that the numbers corresponding to regions can change over time, so if you want to enter a number for the region selection instead, just make sure it still corresponds to your desired area!)

4. You'll also want to add a file named Procfile (no extension) with the following text:

`web: gunicorn app:server`

(This line came from https://dash.plotly.com/deployment .)

I was prompted to enter this line after seeing the following error message within my Google Cloud Console log:

`Step #1: [builder] failed to build: for Python, provide a main.py file or set an entrypoint with "GOOGLE_ENTRYPOINT" env var or by creating a "Procfile" file"`

5. Hopefully, after Google Cloud finishes processing your deployment request, you'll see a message like the following:

`Service [simpleappwithoutlogin] revision [simpleappwithoutlogin-00012-55f] has been deployed and is serving 100 percent of traffic.
Service URL: https://simpleappwithoutlogin-470317599391.us-central1.run.app`

To confirm that your page is operating correctly, visit its service URL (e.g. https://simpleappwithoutlogin-470317599391.us-central1.run.app/ for this app). Ideally, you'll see the same screen that you would when deploying the app locally. 

If you instead see a black screen with 'Service Unavailable' at the top left corner, don't panic! (I got this screen many, many times when learning how to upload Dash apps to the cloud.) This message simply means that something about your deployment that is not quite correct. Perhaps you forgot to include a library within requirements.txt that your script uses, for instance. Make sure to check your logs (available at https://console.cloud.google.com/logs/) for clues as to what might be going wrong with your script.

(For example, seeing "ModuleNotFoundError: No module named 'pandas'" within my log after one failed deployment made me realize that I had forgotten to add pandas to my requirements.txt file.)

If you receive a message like "service account 13371337-compute@developer.gserviceaccount.com does not have access to the bucket," try entering `gcloud auth login` and redoing the login procedure (as suggested by StackOverflow user Lee here: https://stackoverflow.com/a/70377891/13097194 ).

6. After deploying a new version of your app, you may want to delete the old version (especially if it failed to run to begin with) in order to save costs. You can do so by searching for 'Artifact Registry' within the Cloud Console website; navigating to the list of containers for your site; and then keeping only the most recent container. Likewise, you may want to keep only the most recent bucket within the source/ folder in your Cloud Storage bucket. (To delete the other ones, search for 'Buckets' within your Cloud Console; click on your bucket name; click on the 'source/' folder; and then delete all but the most recent bucket.)

#### Using a Cloud Run secret to retrieve data from a Google Sheets document

This app retrieves data from a Google Sheets file called 'Hourly VA Weather Data'; it's located at https://docs.google.com/spreadsheets/d/17aDJ3mg49-n0IEnDgN7ZB85pO87fiUpkZPULYDB8dmo/edit?usp=sharing; this file gets updated on an hourly basis by a laptop running updatintg_online_spreadsheets.py within the Updating Online Spreadsheets section of Python for Nonprofits. (Reference that section for more information about using gspread.) 

In order for the app to connect to that spreadsheet, it retrieves a set of Google service account credentials (which are required for retrieving data from Google Sheets) from a secret stored within a Cloud Run volume. I referenced https://cloud.google.com/run/docs/configuring/services/secrets in the process of enabling this functionality. Secrets can be accessed by Cloud Run either through a path to a volume or through an environment variable; although I chose the former, the latter might actually be more straightforward to set up. 

In order to get this code to work, you'll want to follow the same steps shown within the above link to add your own service account to Cloud Run. You'll also need to make sure that your compute service account has been granted the Secret Manager Secret Accessor role. More information about that step can be found at https://cloud.google.com/secret-manager/docs/manage-access-to-secrets .

If you decide to access your secret through a volume, you can find the path to enter within your code by clicking on your Cloud Run service; selecting 'Edit & Deploy New Revision'; and clicking on 'VOLUME MOUNTS' within the Edit Container menu. The path to use within your code (in my case, '/svcacctsecret/kjb3server_service_account' was listed under 'Mount path.'

**Note:** In my case, the service account whose credentials I uploaded into Cloud Run is the same account that my laptop is using to update the Hourly VA Weather Data workbook. (The content of my 'secret' is simply the .json file containing the account's key that I downloaded in the process of building out my Updating Online Spreadsheets code.) However, it looks like you can also simply use the service account built into your Cloud Run instance; see https://stackoverflow.com/questions/65128196/is-there-a-way-to-authenticate-gspread-with-the-default-service-account for more information. 

Using your built-in Cloud Run service account should allow you to bypass the hassle of storing a service account key as a secret. However, it's still ideal to learn how to use Cloud Run secrets in case you'll ever need to connect to a SQL database within a Dash app. (You could store that database's password as a secret, which should be much more secure than storing it as plain text within your code.)


#### Folder structure

(Note that Procfile is a file without a specified extension rather than a folder.)


readme.md [this file]

app.py

Procfile

requirements.txt

