#!/bin/bash

# It appears that the line above needs to be the first entry within this script.

# NOTE: This copy of the script is meant to be run when your regular server is not active.

# For a discussion of the above line,
# see: https://stackoverflow.com/questions/8967902/why-do-you-need-to-
# put-bin-bash-at-the-beginning-of-a-script-file

echo "Activating Python environment:"

# Activating my custom Python for Nonprofits environment:
# (You may be able to delete the following two lines if you're planning
# to execute the notebook within your base environment.)
# These lines are based on Lamma's post at:
# https://stackoverflow.com/a/60523131/13097194


source ~/miniforge3/etc/profile.d/conda.sh
conda activate pfnv2

# Navigating to the folder that hosts this script:

cd '/home/kjb3/D1V1/kjb3docs/Programming/py/kjb3_programs_2/pfn_2/Updating_Online_Spreadsheets'

# Executing the Python script:

ipython updating_online_spreadsheets.ipynb

echo "Copying weather data to KJB3Server Google Drive folder:"

cp -r weather_data /home/kjb3/kjb3server_drive/


echo "Finished running script."
sleep 2
