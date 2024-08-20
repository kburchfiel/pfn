# Data import script:
# This script will import datasets that will be used by multiple pages.
# Taking care of these imports here should make the site more efficient by
# reducing the number of times each dataset needs to be imported.

import pandas as pd

def improve_col_display(df):
    '''This function replaces underscores in column names with spaces
    and also converts them to title space, thus improving their
    appearance within chart titles. 
    Since some values (e.g. 'ID') are best capitalized rather than
    converted to title case, the function also includes a 
    df.rename() col. This can be expanded as needed to address any
    issues caused by the title case conversion.
    '''
    df.columns = [column.replace('_', ' ').title() 
                  for column in df.columns]
    df.rename(
        columns = {'Student Id':'Student ID'}, inplace = True)


df_curr_enrollment = pd.read_csv(
    'https://raw.githubusercontent.com/kburchfiel/\
pfn/main/Appendix/curr_enrollment.csv')
print("Imported current enrollment data.") # ALlows us to check how many
# times this data will get imported during the web app's operation
# Adding a 'Count' column (which will be useful for pivot tables):
improve_col_display(df_curr_enrollment)
df_curr_enrollment['Count'] = 1

df_survey_results = pd.read_csv('https://raw.githubusercontent.com/\
kburchfiel/pfn/main/Appendix/survey_results.csv')
print("Imported survey results.")
improve_col_display(df_survey_results)
df_survey_results['Count'] = 1

# Merging our survey and enrollment data together in order to allow
# survey results to be compared by college, level, etc.:
df_survey_results_extra_data = df_survey_results.drop('Count', axis = 1).merge(
    df_curr_enrollment, on = 'Student ID', how = 'left')[
['Starting Year', 'Season', 'Score', 'Gender', 'Matriculation Year',
 'College', 'Class Of', 'Level', 'Level For Sorting', 'Count']]
df_survey_results_extra_data
print("Merged enrollment and survey data together to create \
df_survey_results_extra_data.")