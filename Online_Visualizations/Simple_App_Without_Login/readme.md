# Simple App Without Login

## Readme

(Note: the Cloud Run-hosted version of this app can be found at https://simpleappwithoutlogin-470317599391.us-central1.run.app/ .)

This folder provides sample code for a Dash app that can be deployed to Cloud Run. This code was based on the app deployment steps found in https://dash.plotly.com/deployment and https://cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-python-service . (The Plotly walkthrough shows how to deploy a Dash app to Heroku, and the Cloud Run walkthrough shows how to deploy a Flask App to Cloud Run; by taking bits from each, you can then learn how to deploy a *Dash* app to *Cloud Run.* :)

### Using a Cloud Run Secret to Retrieve Data From a Google Sheets Document

This app retrieves data from a Google Sheets file called 'Hourly VA Weather Data'; it's located at https://docs.google.com/spreadsheets/d/17aDJ3mg49-n0IEnDgN7ZB85pO87fiUpkZPULYDB8dmo/edit?usp=sharing; this file gets updated on an hourly basis by a laptop running updatintg_online_spreadsheets.py within the Updating Online Spreadsheets section of Python for Nonprofits. (Reference that section for more information about using gspread.) 

In order for the app to connect to that spreadsheet, it retrieves a set of Google service account credentials (which are required for retrieving data from Google Sheets) from a secret stored within a Cloud Run volume. I referenced https://cloud.google.com/run/docs/configuring/services/secrets in the process of enabling this functionality. Secrets can be accessed by Cloud Run either through a path to a volume or through an environment variable; although I chose the former, the latter might actually be more straightforward to set up. 

In order to get this code to work, you'll want to follow the same steps shown within the above link to add your own service account to Cloud Run. You'll also need to make sure that your compute service account has been granted the Secret Manager Secret Accessor role. More information about that step can be found at https://cloud.google.com/secret-manager/docs/manage-access-to-secrets .

If you decide to access your secret through a volume, you can find the path to enter within your code by clicking on your Cloud Run service; selecting 'Edit & Deploy New Revision'; and clicking on 'VOLUME MOUNTS' within the Edit Container menu. The path to use within your code (in my case, '/svcacctsecret/kjb3server_service_account' was listed under 'Mount path.'

**Note:** In my case, the service account whose credentials I uploaded into Cloud Run is the same account that my laptop is using to update the Hourly VA Weather Data workbook. (The content of my 'secret' is simply the .json file containing the account's key that I downloaded in the process of building out my Updating Online Spreadsheets code.) However, it looks like you can also simply use the service account built into your Cloud Run instance; see https://stackoverflow.com/questions/65128196/is-there-a-way-to-authenticate-gspread-with-the-default-service-account for more information. 

Using your built-in Cloud Run service account should allow you to bypass the hassle of storing a service account key as a secret. However, it's still ideal to learn how to use Cloud Run secrets in case you'll ever need to connect to a SQL database within a Dash app. (You could store that database's password as a secret, which should be much more secure than storing it as plain text within your code.)

### Folder structure


readme.md [this file]

app.py

Procfile

requirements.txt