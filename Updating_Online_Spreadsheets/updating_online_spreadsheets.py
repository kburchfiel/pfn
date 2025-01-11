#!/usr/bin/env python
# coding: utf-8

# # Updating Online Spreadsheets
# 
# This script will demonstrate how to upload the contents of a DataFrame into a Google Sheets file using Python's `gspread` and `gspread-dataframe` libraries. This is a convenient option for sharing your output with others, especially if you need to update that output on a regular basis.
# 
# The Google Sheets worksheet that this script will update can be found at https://docs.google.com/spreadsheets/d/17aDJ3mg49-n0IEnDgN7ZB85pO87fiUpkZPULYDB8dmo/edit?usp=sharing .
# 
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


# ## Importing new weather data for three Virginia weather stations; combining it with pre-existing data; and then saving a revised copy of this table to a .csv file:

# In[5]:


data_folder = 'weather_data'


# ### Importing weather data for Charlottesville:

# In[6]:


print("Downloading KCHO data.")


# In[7]:


weather_import(
    station_code = 'KCHO',
    data_folder = data_folder)


# ### Importing weather data for Dulles International Airport:

# In[8]:


print("Downloading KIAD data.")


# In[9]:


weather_import(
    station_code = 'KIAD',
    data_folder = data_folder)


# ### Importing weather data for Winchester:
# 
# (This data appears to be recorded at 20-minute intervals rather than hourly ones.)

# In[10]:


print("Downloading KOKV data.")


# In[11]:


test_df = weather_import(
    station_code = 'KOKV',
    data_folder = data_folder)
test_df


# ## Reading these datasets into DataFrames:

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


# ## Importing these DataFrames into a Google Sheets workbook:

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


# ## Performing the same data export steps for KIAD and KOKV data:

# In[20]:


ws = wb.worksheet('KIAD')
ws.clear() 
set_with_dataframe(ws, df_weather_kiad.iloc[-960:])

ws = wb.worksheet('KOKV')
ws.clear() 
set_with_dataframe(ws, df_weather_kokv.iloc[-960:])

