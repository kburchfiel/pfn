#!/usr/bin/env python
# coding: utf-8

# # Updating Online Spreadsheets
# 
# This script will demonstrate how to upload the contents of a DataFrame into a Google Sheets file using Python's `gspread` and `gspread-dataframe` libraries. This is a convenient option for sharing your output with others, especially if you need to update that output on a regular basis.
# 
# The Google Sheets worksheet that this script will update can be found at https://docs.google.com/spreadsheets/d/17aDJ3mg49-n0IEnDgN7ZB85pO87fiUpkZPULYDB8dmo/edit?usp=sharing .
# 
# Since the NWS weather data accessed by this script generally gets updated on an hourly basis, it makes sense to have this script run automatically every hour. That way, your Google Sheets data, along with your local .csv copies of historical weather data, will always be relatively up to date. To automate this script, I recommend saving it as a .py file (which is easy to do within JupyterLab Desktop); setting up a script that will run this file; and then having your computer run this script on an hourly basis. (More information on accomplishing these steps within Linux can be found at the end of this notebook.)
# 
# ## Prerequisites
# 
# 1. Python's gspread library provides a very helpful overview of connecting to Google Sheets workbooks via a service account at https://docs.gspread.org/en/latest/oauth2.html#for-bots-using-service-account . (There are multiple ways to connect to workbooks, but I find the service account approach to be pretty straightforward.) Go ahead and complete these steps if you haven't already. (Note: I chose to save my service account key to a custom path rather than the default one specified in the documentation; that way, I could more easily work with multiple account keys on my computer.) Also make sure that, prior to enabling the Google Sheets and Google Drive APIs, the Google Cloud project that you want to use for this script has been selected.
# 
# 2. If you also specified a custom path, you'll need to create a file called 'service_key_path.txt' within this folder that points to it. That way, the following cell will be able to read in its location for use within gspread functions. (Alternatively, you could simply replace the following cell's code with `service_key_path = (path_to_your_key)`. Or, if you're using the default key location, you can comment out this cell altogether.)
# 
# 3. As noted in the gspread service account documentation, you'll need to give the email associated with your service account editor access to the Google Sheets workbook that you'd like your script to update. (This email is *not* the same as your regular Google Email; it will likely look something like accountname@cloudprojectname.iam.gserviceaccount.com. You can find it within your service account file.

# In[1]:


import sys
sys.path.insert(1, '../Appendix')
from helper_funcs import config_notebook, wadi
display_type = config_notebook(display_max_columns = 5)
# Specifying which columns to render within the output:
display_cols = ['Station', 'Date/Time', 'Temp', 
                '1-Hour Precip', 'Rolling 24-Hour Precip']

with open('service_key_path.txt') as file:
    service_key_path = file.read()


# In[2]:


import gspread
from gspread_dataframe import set_with_dataframe, get_as_dataframe
# From https://pypi.org/project/gspread-dataframe/
# gspread_dataframe isn't available within conda-forge as of 2025-02-20;
# therefore, you'll need to install it via the following pip command:
# pip install gspread-dataframe


# (If you're using gspread's default path, you can comment out the first line and then uncomment the following one.)

# In[3]:


gc = gspread.service_account(filename=service_key_path)

# gc = gspread.service_account()

# (This code comes from
# # From https://docs.gspread.org/en/latest/index.html)


# Importing additional libraries:
# 
# (Note: the weather_import.py file imported below derives from recent_weather_data.ipynb within the Automated_Notebooks section of Python for Nonprofits.)

# In[4]:


import pandas as pd
from weather_import import weather_import


# ## Importing weather data
# 
# The following cells will import weather data for three Virginia weather stations; combine it with pre-existing data; and then save a revised copy of this table to a .csv file.

# In[5]:


data_folder = 'weather_data'


# ### Importing weather data for Charlottesville

# In[6]:


print("Downloading KCHO data.")


# In[7]:


weather_import(
    station_code = 'KCHO',
    data_folder = data_folder)


# ### Importing weather data for Dulles International Airport

# In[8]:


print("Downloading KIAD data.")


# In[9]:


weather_import(
    station_code = 'KIAD',
    data_folder = data_folder)


# ### Importing weather data for Winchester
# 
# (This data appears to be recorded at 20-minute intervals rather than hourly ones.)

# In[10]:


print("Downloading KOKV data.")


# In[11]:


test_df = weather_import(
    station_code = 'KOKV',
    data_folder = data_folder)
test_df


# ## Reading these datasets into DataFrames

# In[12]:


df_weather_kcho = pd.read_csv(
    data_folder+'/'+'KCHO'+'_'
    +'historical_hourly_data_updated.csv')
df_weather_kcho[display_cols].tail()


# In[13]:


df_weather_kiad = pd.read_csv(
    data_folder+'/'+'KIAD'+'_'
    +'historical_hourly_data_updated.csv')
df_weather_kiad[display_cols].tail()


# In[14]:


df_weather_kokv = pd.read_csv(
    data_folder+'/'+'KOKV'+'_'
    +'historical_hourly_data_updated.csv')
df_weather_kokv[display_cols].tail()


# ## Importing these DataFrames into a Google Sheets workbook

# In order to export these datasets to a Google Sheets workbook, we'll first need to open that workbook with gspread. There are a few ways to do this (see https://docs.gspread.org/en/latest/user-guide.html#opening-a-spreadsheet for reference), but I like the `open_by_key()` option, which allows you--as the function's name suggests--to open a workbook using its key.
# 
# These keys are located within the center of each workbook URL. For instance, the full URL of the workbook I'll be updating is `https://docs.google.com/spreadsheets/d/17aDJ3mg49-n0IEnDgN7ZB85pO87fiUpkZPULYDB8dmo/edit?usp=sharing`, so the key--located in between the `/d/` component of that URL and the following `/`--is `17aDJ3mg49-n0IEnDgN7ZB85pO87fiUpkZPULYDB8dmo`.

# In[15]:


wb = gc.open_by_key('17aDJ3mg49-n0IEnDgN7ZB85pO87fiUpkZPULYDB8dmo')
# Based on 
# https://docs.gspread.org/en/latest/user-guide.html#opening-a-spreadsheet
wb


# Next, I'll select the 'KCHO' worksheet within this workbook, as that's the first one I'd like to update. I'll also clear out the current contents using `ws.clear()`; that way, only the latest DataFrame contents will appear within the spreadsheet after I call `set_with_dataframe` below. (If the most recent DataFrame is smaller than the previous version, parts of the previous one would still appear unless `ws.clear()` is called.

# In[16]:


ws = wb.worksheet('KCHO')
# https://docs.gspread.org/en/latest/user-guide.html#opening-a-spreadsheet


# In[17]:


ws.clear() 
ws


# Finally, I'll call `set_with_dataframe` to export this DataFrame to df_weather.

# In[18]:


# Only the most recent 960 rows (representing 40 days' worth of data if
# no entries were missing) will get exported to Google Sheets. This will
# limit the time (and potentially money) needed to import this data
# into a Dash app (https://github.com/kburchfiel/pfn/tree/
# main/Online_Visualizations/Simple_App_Without_Login)
# that utilizes it.
set_with_dataframe(ws, df_weather_kcho.iloc[-960:])
# Source: https://pypi.org/project/gspread-dataframe/


# In order to confirm that this upload was successful, we can call `get_as_dataframe` to import the contents of the worksheet into a new DataFrame:

# In[19]:


df_weather_from_ws = get_as_dataframe(ws)
df_weather_from_ws[display_cols].tail()


# ### Performing the same data export steps for KIAD and KOKV data

# In[20]:


ws = wb.worksheet('KIAD')
ws.clear() 
set_with_dataframe(ws, df_weather_kiad.iloc[-960:])

ws = wb.worksheet('KOKV')
ws.clear() 
set_with_dataframe(ws, df_weather_kokv.iloc[-960:])


# ## Appendix: A shell script and crontab entry for running this notebook automatically
# 
# (These steps were written for Linux environments, but Windows also supports automated script operation; you'd just need to write a batch script rather than a shell script and use Windows Task Scheduler instead of your cron editor.)
# 
# Your computer is more than happy to run a .py equivalent of this script, rain or shine, every hour of the day (as long as it's powered on, of course). How can you tell it to do so? First, you'll need to create a shell script that activates your Python environment; navigates to the folder containing the .py version of this notebook*; and then runs that file. 
# 
# Here's what this script looks like on my computer: (I gave it the imaginative name *online_spreadsheet_update.sh.*)
# 
# \* *(To create a .py version of this notebook, open it within JupyterLab Desktop; navigate to File --> Save and Export Notebook As --> Executable Script; and then save it (preferably within the same folder as updating_online_spreadsheets.ipynb) as updating_online_spreadsheets.py. You could also just run the .ipynb file directly if you'd prefer; see the comments within the following script for more details.)*

# ```
# #!/bin/bash
# 
# # It appears that the line above needs to be the first entry within this script.
# 
# # For a discussion of the above line,
# # see: https://stackoverflow.com/questions/8967902/why-do-you-need-to-put-bin-bash-st-the-beginning-of-a-script-file
# 
# echo "Activating Python environment:"
# 
# # Activating my custom Python for Nonprofits environment:
# # (You may be able to delete the following two lines if you're planning
# # to execute the notebook within your base environment.)
# # These lines are based on Lamma's post at:
# # https://stackoverflow.com/a/60523131/13097194
# 
# source ~/miniforge3/etc/profile.d/conda.sh
# conda activate kjb3server
# 
# # Navigating to the folder that hosts this script:
# 
# cd /home/kjb3lxms/kjb3python/Updating_Online_Spreadsheets
# 
# # Executing the Python script:
# 
# python updating_online_spreadsheets.py
# 
# # To instead execute the original Jupyter notebook, run:
# # ipython updating_online_spreadsheets.ipynb
# 
# echo "Finished running script."
# sleep 2
# ```

# In order to instruct your computer to run this script 10 minutes after each hour, you can then run `crontab -e` within your terminal and paste the following line at the bottom of the page: (You'll of course need to replace my path with your own path to this file.)
# 
# *(If you're new to crontabs, make sure to review the documentation that appears at the top of your crontab file. Also, if you're working within the Nano editor, make sure to hit Ctrl + X to exit out of the editor after your updates have been saved; if you instead close the window, your changes won't be saved.)*

# ```
# 10 * * * * /home/kjb3lxms/kjb3python/Updating_Online_Spreadsheets/online_spreadsheet_update.sh
# ```
