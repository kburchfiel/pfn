# Data import script:
# This script will import datasets that will be used by multiple pages.
# Taking care of these imports here *may* make the site more efficient 
# by reducing the number of times each dataset needs to be imported.

offline_import = False # Allows for source data to get read in locally,
# which may improve performance when debugging or editing the code. 
# (This should be set to False prior to deploying this app online.)

import pandas as pd

def improve_col_display(df):
    '''This function replaces underscores in column names with spaces
    and also converts them to title space, thus improving their
    appearance within chart titles. 
    Since some values (e.g. 'ID') are best capitalized rather than
    converted to title case, the function also includes a 
    df.rename() call. This can be expanded as needed to address any other
    issues caused by the blanket title case conversion that precedes it.
    '''
    df.columns = [column.replace('_', ' ').title() 
                  for column in df.columns]
    df.rename(
        columns = {'Student Id':'Student ID'}, inplace = True)

if offline_import == True: # In this case, the source data will get 
    # imported from a local file.
    print("Importing source data from local .csv files.")
    df_curr_enrollment = pd.read_csv(
        '../../Appendix/curr_enrollment.csv')
    df_survey_results = pd.read_csv(
        '../../Appendix/survey_results.csv')
else:
    print("Downloading source data from an online source.")
    df_curr_enrollment = pd.read_csv(
        'https://raw.githubusercontent.com/kburchfiel/\
pfn/main/Appendix/curr_enrollment.csv')
    df_survey_results = pd.read_csv('https://raw.githubusercontent.com/\
kburchfiel/pfn/main/Appendix/survey_results.csv')

print("Imported current enrollment data.") # Allows us to check how many
# times this data will get imported during the web app's operation
print("Imported survey results.")

# Adding an 'Enrollment' column (which will be useful for pivot tables)
# and chart titles:
improve_col_display(df_curr_enrollment)
df_curr_enrollment['Enrollment'] = 1

improve_col_display(df_survey_results)
df_survey_results['Count'] = 1

# Merging our survey and enrollment data together in order to allow
# survey results to be compared by college, level, etc.:
df_survey_results_extra_data = df_survey_results.merge(
    df_curr_enrollment, on = 'Student ID', how = 'left')[
['Starting Year', 'Season', 'Score', 'Gender', 'Matriculation Year',
 'College', 'Class Of', 'Level', 'Level For Sorting']]

print("Merged enrollment and survey data together to create \
df_survey_results_extra_data.")