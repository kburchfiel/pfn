# Weather Data Import
# By Kenneth Burchfiel
# Released under the MIT license

import pandas as pd
import os
import numpy as np
from datetime import datetime, timedelta

def weather_import(station_code, data_folder = ''):
    '''This function retrieves National Weather Service (NWS) hourly 
    weather data for the last 
    3 days for the station specified in station_code; adds it to
    pre-existing data (if any); and then saves this data to
    the folder specified in data_folder. 
    (Specifying a data folder is optional; if none is specified, files
    will simply be saved to the current working directory.)'''
    if len(data_folder) > 0:
        post_folder_char = '/'
    else:
        post_folder_char = ''
    today = datetime.today().date()
    retrieval_date = str(today) # The date on which the current set of 
    # 3-day weather data is being retrieved. Note that this date won't
    # match the dates for earlier records within this dataset.
    
    # Importing the latest set of hourly observations from the 
    # National Weather Service:

    # read_html returns a list of tables (even though only one table is 
    # currently present on this site), so we'll use [0] to access that
    # table.
    # The final 3 rows are simply a repetition of the header, so I added in
    # [:-3] to exclude them from the DataFrame.
    # header = 2 specifies that the third row in the DataFrame should be 
    # used as a header. (The first two rows' values are mostly duplicates
    # of this row's data.)
    
    df_3day_data = pd.read_html(
    f'https://forecast.weather.gov/data/obhistory/{station_code}.html',
    header = 2)[0][:-3]
    df_3day_data.tail()

    # The observation time column within this dataset shows the time zone; 
    # this will cause issues when daylight savings time begins or ends 
    # (as those events will cause the column name to change). To prevent 
    # this from causing any issues when combining our latest data with 
    # our historical dataset, we'll add this time zone data to a 
    # separate column, then rename the original time column to 'Time.'

    original_time_col = [
        column for column in df_3day_data.columns if 'Time' in column][0]

    # Extracting the time zone from this column, then converting it to
    # uppercase:
    tz = original_time_col.split(' (')[1].split(')')[0].upper()

    df_3day_data.rename(columns={original_time_col:'Time', 'Date':'Day'}, 
                        inplace = True)
    df_3day_data.insert(2, 'Time Zone', tz)
    df_3day_data['Day'] = df_3day_data['Day'].astype('int')
    df_3day_data['Data Retrieval Date'] = pd.to_datetime(
        datetime.today().date())
    
    ## Determining the year and month of each observation:
    
    # The original NWS dataset only shows the day of the month for each row 
    # (which is understandable, since it only contains data for the most 
    # recent 72 hours; thus, the year and month can easily be inferred). 
    # However, because we'll be keeping a historical copy of this data, 
    # calculating each observation's corresponding year and month will 
    # be crucial for avoiding ambiguous results.
    
    # We'll use the following approach to generate a YYYY-MM-DD-formatted 
    # 'Date' column for each observation:
    
    # 1. We'll use the year and month found within our Data Retrieval Date 
    # column as a basis for our observation years and months.
    
    # 2. If the observation day is less than the day within our Data 
    # Retrieval Date column, we'll assume that that observation took place 
    # within the current month; otherwise, we'll assume it took place 
    # during the previous month and thus reduce the observation month 
    # by 1. (For instance, an observation day of 5 and a data retrieval 
    # day of 6 would indicate that the observation and data retrieval 
    # months are the same; meanwhile, an observation day of 31 and a data
    # retrieval day of 2 demonstrates that the observation took place 
    # during the previous month.)
    
    # 3. The previous step will result in an observation month of 0 if 
    # data for December were retrieved in January. In this case, we'll 
    # decrease the observation year by 1 and switch the observation 
    # month to 12. Otherwise, we'll use the data retrieval year 
    # as our observation year.
    
    # 4. Finally, we'll add these observation month and years to the 
    # pre-existing observation day column in order to produce a new 
    # 'Date' column in YYYY-MM-DD format.

    df_3day_data['Data Retrieval Date'] = pd.to_datetime(
        df_3day_data['Data Retrieval Date'])
    
    df_3day_data['Obs_Month'] = np.where(
        df_3day_data['Day'] <= df_3day_data['Data Retrieval Date'].dt.day, 
        df_3day_data['Data Retrieval Date'].dt.month, 
        df_3day_data['Data Retrieval Date'].dt.month -1)
    
    df_3day_data['Obs_Year'] = np.where(
        df_3day_data['Obs_Month'] != 0,
        df_3day_data['Data Retrieval Date'].dt.year, 
        df_3day_data['Data Retrieval Date'].dt.year-1)
    
    df_3day_data['Obs_Month'] = df_3day_data['Obs_Month'].replace(
        0, 12).copy()
    
    # Creating our Date column:
    # Note the use of str.zfill() to add a leading 0 to single-digit
    # months and dates (which will make it easier to sort them in 
    # chronological order).
    df_3day_data.insert(0, 'Date', (
        df_3day_data['Obs_Year'].astype('str') + '-' +
        df_3day_data['Obs_Month'].astype('str').str.zfill(2) + '-' +
        df_3day_data['Day'].astype('str').str.zfill(2)))
    
    # Sorting the dataset chronologically:
    df_3day_data.sort_values(['Date', 'Time'], inplace = True)
    df_3day_data

    # Saving this data to a .csv file:
    df_3day_data.to_csv(
        f'{data_folder}{post_folder_char}{station_code}\
_most_recent_3_day_data.csv', 
        index = False)

    # Next, the function will append new data within this file to 
    # a historical dataset. If such a dataset doesn't exist already,
    # it will get created shortly.
    # Determining which argument to pass to os.listdir(): (This argument
    # should be None if no data_folder value was provided so as not 
    # to raise an error.)
    
    if len(data_folder) > 0:
        listdir_arg = data_folder
    else:
        listdir_arg = None
    if f'{station_code}_historical_hourly_data.csv' not in os.listdir(
        listdir_arg):
        
        print("Historical copy of this dataset doesn't yet exist. \
Initializing it as a copy of the 3-day dataset.")
        df_3day_data.to_csv(
            f'{data_folder}{post_folder_char}{station_code}\
_historical_hourly_data.csv', index = False)
              
    # Reading in historical weather data:
    
    df_historical_data = pd.read_csv(
        f'{data_folder}{post_folder_char}\
{station_code}_historical_hourly_data.csv')   
    print("Original length of historical data file:",
          len(df_historical_data))
    
    # Recreating df_3day_data by importing the .csv copy of the table 
    # that the function just created:
    
    # (This step may appear unnecessary, but it does help ensure that 
    #  both this data and that found in df_historical_data will use 
    #  the same data types.)

    df_3day_data = pd.read_csv(f'{data_folder}{post_folder_char}\
{station_code}_most_recent_3_day_data.csv')

    # Combining historical data with the latest 3-day dataset:
    
    df_wx = pd.concat([df_historical_data, df_3day_data])
    # Storing the station code within the DataFrame:
    df_wx['Station'] = station_code
    
    # The function will now remove duplicate Date/Time entries.
    
    # Calculating the 24-digit hour corresponding to each DataFrame:
    # (This code assumes that a 24-hour clock is being used to display
    # times.)
    df_wx['Hour'] = df_wx['Time'].str.split(
        ':').str[0].astype('int')

    # Keeping only one result per date and hour:
    # (This approach will prove useful when using .rolling() to calculate
    # rainfall totals for specific periods, as it will allow us to
    # assume that N rows of data represent N hours. However, 
    # at least one NWS station (KOKV) reports recent weather data
    # every 20 minutes; only one in three of such reports will get
    # retained after drop_duplicates() gets called. 
    df_wx.drop_duplicates(
        ['Date', 'Hour'], keep = 'last', inplace = True)
    # This isn't a perfect approach, as it will likely cause an 
    # hour of data to get lost when Daylight Savings Time ends.
     
    print("New length of historical data file:",
          len(df_wx))

    # Saving this updated copy of df_wx to a .csv file:
    df_wx.to_csv(
        f'{data_folder}{post_folder_char}\
{station_code}_historical_hourly_data.csv', index = False)

    ## Making further updates to this combined dataset:

    # Removing percentages from Relative Humidity column so that these
    # values can be converted to floats:
    
    df_wx['Relative Humidity'] = df_wx[
    'Relative Humidity'].str.replace('%','')
    
    # Converting numerical data in certain columns to floats:
    
    for column in ['Air', 'Dwpt', 'altimeter (in)', 'sea level (mb)',
                   '1 hr', '3 hr', '6 hr', 'Relative Humidity']:
        df_wx[column] = df_wx[column].astype(
            'float')
    
    # Replacing NaN precipitation values with 0s:
    for column in ['1 hr', '3 hr', '6 hr']:
        df_wx[column] = df_wx[
        column].fillna(0).copy()
       
    # Adding 'Precip' prefixes to the hourly precipitation rows; making the 
    # temperature and dew point column names more intuitive; and removing
    # time zone data from the time field:
    df_wx.rename(columns = {
        '1 hr':'1-Hour Precip',
        '3 hr':'3-Hour Precip',
        '6 hr':'6-Hour Precip',
        'Air':'Temp',
        'Dwpt':'Dew Point',
        'altimeter (in)':'Altimeter (in.)',
    original_time_col:'Time'},
         inplace = True)
    
    # Sorting the table in chronological order:
    
    df_wx.sort_values(['Date', 'Time'], inplace = True)
    df_wx.reset_index(drop=True,inplace=True)

    # Adding columns that show cumulative precipitation totals for various
    # periods: (These all update every hour unlike the built-in
    # NWS hourly precipitation totals. However, they're also 
    # susceptible to errors caused by missing rows.)
    for hourly_interval in [3, 6, 12, 24]:
        df_wx[f'Rolling {hourly_interval}-Hour Precip'] = (
            df_wx['1-Hour Precip'].rolling(
                window=hourly_interval).sum())

    # Adding a windspeed column:
    # This code assumes that the 'Wind (mph)' column within the original
    # dataset uses the following formats:
    # 'Calm' (when no wind was reported)
    # DIRECTION WINDSPEED (e.g. 'W 8') when wind, but no gusts, were
    # reported
    # DIRECTION WINDSPEED GUST_DIRECTION GUST_SPEED (e.g. 'W 28 G 40')
    # when both wind and gusts were reported
    # The following code uses str.split() and str[1] to retrieve the 
    # second item within these reports, as this item should always be
    # the windspeed (rather than the gust speed). 
    
    df_wx['Windspeed'] = df_wx['Wind (mph)'].str.split('  ').str[
    1]

    # For 'Calm' readings,
    # str[1] will be NaN, and thus we can replace those values with 0.

    df_wx['Windspeed'] = np.where(df_wx['Wind (mph)'] == 'Calm',
                                  0, df_wx['Windspeed'])
    
    # Removing the 6-hour max and min temperature columns in order to 
    # simplify the table:
    df_wx.drop(['Max.', 'Min.'], axis = 1, inplace = True)
        
    # Creating a 'Date/Time' column for graphing purposes:
    
    df_wx.insert(
        2, 'Date/Time', df_wx['Date'].astype('str') 
        + ' ' + df_wx['Time'].astype('str'))
    
    # Saving this revised dataset to a .csv file so that it can be 
    # visualized and shared with others:

    df_wx.to_csv(f'{data_folder}{post_folder_char}\
{station_code}_historical_hourly_data_updated.csv', index = False)
