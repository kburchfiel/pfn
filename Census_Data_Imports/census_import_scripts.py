# Census Data Import Scripts

# By Kenneth Burchfiel

# Released under the MIT License

# This Python file creates scripts for creating lists of American
# Community Survey variables; generating aliases for variable codes;
# using the Census API to download data; and adding certain statistical
# fields to tables.

import pandas as pd
from iteration_utilities import duplicates

def download_variable_list(year, survey):
    '''This function imports a list of all variables from the Census
    website, thus allowing variable codes to get mapped to names in 
    subsequent analyses.
    year: the year for which to retrieve variables.
    survey: the ACS type for which to retrieve variables (e.g.
    'acs5' or 'acs1' for the 5-year and 1-year ACS estimates,
    respectively.)
    '''
    print(f"Importing {survey} variables from {year}.")
    df_variables_page = pd.read_html(
        f'https://api.census.gov/data/\
{year}/acs/{survey}/variables.html')[0] 
    # [0] selects the first HTML table found on this page.
    # See https://pandas.pydata.org/pandas-docs/stable/reference/api/
    # pandas.read_html.html
    # for more information on pd.read_html().
        
    # Some rows in this table contain items other than demographic 
    # variables (e.g. region names). We can exclude them by selecting 
    # only rows that begin with 'Estimate'. (Another option would have 
    # been to filter out rows with N/A 'Group' entries (i.e. 
    # df_variables.query("Group.isna() == False")), 
    # but this would have left a couple non-variable rows in place.
    
    df_variables = df_variables_page[
    df_variables_page['Label'].str[0:8] == 'Estimate'].copy(
    ).reset_index(drop=True)
    # Removing an extraneous column from our output
    if 'Unnamed: 8' in df_variables.columns:
        df_variables.drop('Unnamed: 8', axis = 1, inplace = True)
    # Saving this table to a local .csv file:
    df_variables.to_csv(f'Datasets/{survey}_{year}_variables.csv',
                       index = False) 

    # Given that there are tens of thousands of individual variables
    # within the ACS, it could take a very long time to identify 
    # the items you'd like to retrieve from this dataset. 
    # The following code makes this search process somewhat easier by 
    # creating a separate *groups* table that shows only unique group 
    # names and their written descriptions (e.g. 'Sex by Age').
    
    df_groups = df_variables.drop_duplicates(
        'Group')[['Concept', 'Group']].copy(
        ).reset_index(drop=True)
    df_groups.head()

    df_groups.to_csv(f'Datasets/{survey}_{year}_groups.csv', 
                 index = False)

    
    print(f"Finished saving variable and group tables to .csv files.")
    

def create_variable_aliases(df_variables, variable_list):
    '''This function creates a dictionary whose keys are 
    the original 'Name' values (e.g. 'B001_001E') within a variable
    list on the Census API website and whose values are the replacement 
    names (e.g. 'Sex by Age_Estimate!!Total:_B01001_001E').
    This resulting dictionary can then be passed to a df.rename() call
    within retrieve_census_data() in order to make the output of that
    function easier to interpret.
    
    df_variables: A DataFrame containing a list of Census variables. For
    an example of this list for the 2021 American Community Survey (5-Year 
    Estimates), visit: 
    https://api.census.gov/data/2021/acs/acs5/examples.html .
    
    variable_list: The list of variables to rename 
    (e.g. ['B01001_001E', 'B01001_002E']).
    '''
    # Creating a DataFrame that contains the information needed for the
    # updated column names:
    df_aliases = df_variables.query(
        "Name in @variable_list")[['Name', 'Label', 'Concept']].copy()
    # Creating a new 'Description' column that will replace the original
    # output field names:
    df_aliases['Description'] = (df_aliases['Concept'] 
                                 + '_' + df_aliases['Label'] 
                                 + ' (' + df_aliases['Name'] + ')')
    # Creating a dictionary whose keys are the original field names and 
    # whose values are the new 'Description' entries that were 
    # just created:
    alias_dict = df_aliases.set_index('Name').to_dict()['Description']
    # See https://pandas.pydata.org/pandas-docs/stable/reference/api/
    # pandas.DataFrame.to_dict.html
    return alias_dict


def retrieve_census_data(survey, year, region, key, variable_list,
                         rename_data_fields = False, 
                         field_vars_dict = {}):
    '''This function (which I plan to expand) retrieves data from the US
    Census API. It accommodates more than 50 variables.
    
    survey: the survey from which to retrieve data. The only arguments
    currently supported are 'acs5' and 'acs1' (for the American Community 
    Survey 5-Year and 1-Year estimates, respectively).
    
    year: the year for which you wish to retrieve survey data. Note that,
    When region is set to 'acs5', the survey results will include data
    for the 5 years leading up to (and including) the 'year' argument.
    (For example, if you set 'year' to 2021, you'll retrieve ACS5 data
    from 2017 to 2021 (inclusive).)
    
    
    region: The geographic level at which you wish to retrieve data. 
    Examples include 'us', 'state', 'county', 'zip', 'msa' 
    (for metropolitan/micropolitan statistical area data), and 'csa' 
    (for combined statistical area data); 
    however, other regions are supported as well. Consult your survey's 
    API examples page for other options. (For instance, if you wanted to 
    retrieve data by urban area within the 2021 ACS5, you could go to 
    https://api.census.gov/data/2021/acs/acs5/examples.html, then search
    for 'urban area.' The Urban Area URL ends with
    '&for=urban%20area:*&key=YOUR_KEY_GOES_HERE'. Therefore, you'd want to
    use 'urban%20area' as your 'region' argument.)   

    (Note: 'zip' will retrieve results by Zip Code
    Tabulation Area, which are similar to (but not identical to)
    # zip codes. See 
    # https://en.wikipedia.org/wiki/ZIP_Code_Tabulation_Area
    # for more information.
    
    variable_list: The list of variables for which to retrieve data.

    key: your personal Census API key.

    rename_data_fields: set to True to replace column names in your 
    dataset with new entries of your choice.

    field_vars_dict: A dictionary that stores the original variable names
    retrieved by the Census (e.g. 'B01001_001E' as keys and your desired
    replacements as values. Example: 
    {'B01001_001E': 'Sex by Age_Estimate!!Total:_B01001_001E',
     'B01001_002E': 'Sex by Age_Estimate!!Total:!!Male:_B01001_002E'}'
     
    '''

    # Using the iteration_utilities library to check for duplicate
    # values within variable_list (which could cause issues later on):
    # The following code is based on
    # https://iteration-utilities.readthedocs.io/en/latest/generated/
    # duplicates.html
    duplicate_variables = list(duplicates(variable_list))
    
    if len(duplicate_variables) > 0:
        raise ValueError(f"The following variables appear more than once \
in your variable list: {duplicate_variables}")
    
    if survey == 'acs5':
        survey_string = 'acs/acs5'

    elif survey == 'acs1':
        survey_string = 'acs/acs1'
    
    else:
        raise ValueError("This survey type is not currently supported by \
                         the function.")

    
    # Converting simplified region names into strings that the API 
    # function will recognize:
    if region == 'zip':
        region = 'zip%20code%20tabulation%20area' # Based on
        # the ZCTA example within
        # https://api.census.gov/data/2021/acs/acs5/examples.html
    
    if region == 'csa':
        region = 'combined%20statistical%20area'
    
    if region == 'msa':
        region = 'metropolitan%20statistical\
%20area/micropolitan%20statistical%20area'

    
    # Only 50 variables can be retrieved from the Census API at a time 
    # using the approach shown in this function. The following code 
    # accommodates this limitation by splitting variable_list into 
    # sublists of up to 49 variables. The data retrieved for the variables 
    # in these sublists will then get merged back together.
    # (49 variables are retrieved at a time instead of 50 because it 
    # appears that the initial 'NAME' variable also counts towards 
    # the 50-variable limit.)
    
    i = 0
       
    while i < len(variable_list): # i.e. while there
        # are still more variables to iterate through
        variable_sublist = variable_list[i:i+49] # This line reads the 
        # next 49 variables from variable_list into a sublist that can 
        # then be\ passed to the API
        # print("variable_sublist:", variable_sublist)
        # Converting the list of variables into a string that can be 
        # passed to the API call:
        # (The Census API guide at
        # https://www.census.gov/content/dam/Census/data/developers/
        # api-user-guide/api-guide.pdf
        # demonstrates how to call multiple census variables at once.)
        variable_string = ','.join(variable_sublist)
        # print("variable_string:",variable_string)
    
        # Retrieving data via the Census API:
        # This line was originally based on an example found in
        # https://api.census.gov/data/2022/acs/acs5/examples.html .
    
        # read_json documentation:
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/
        # pandas.read_json.html

        api_url = f'https://api.census.gov/data/{year}/\
{survey_string}?get=NAME,{variable_string}&for={region}:*&key={key}'
        # print(api_url)
        
        df_results = pd.read_json(api_url)
    
        # At this point, the DataFrame's columns are a list of integers; 
        # the desired column names are stored within the first row. 
        # The following code resolves this issue by setting these row 
        # values as the column values and then deleting this row.
    
        df_results.columns = df_results.iloc[0]
        df_results.drop(0, inplace = True)


        # Determining which merge keys to use when combining API results
        # for different sublists together:
        # This is made more complicated by the fact that results for 
        # different regions will have different identifier
        # columns (e.g. 'NAME', 'county', and 'state' for county data but 
        # only 'NAME' and 'state' for state data). However, we can 
        # accommodate this behavior by simply initializing our list of 
        # merge keys as the set of all columns that are *not* also 
        # variable columns.
        if i == 0: # This step only needs to be performed for our first
            # sublist of variables, since merge keys for other sublists
            # will be identical.
            merge_keys = list(set(df_results.columns) 
              - set(variable_sublist))
            # print("merge_keys:",merge_keys)

        if i == 0: # Since this is the first set 
            # of results, we can initialize df_combined_results 
            # as a copy of df_results.
            df_combined_results = df_results.copy()
        else: # Merging our latest set of results into df_results:
            df_combined_results = df_combined_results.merge(
                df_results, on = merge_keys,
                how = 'outer').copy()
            # Added .copy() here in response to a data fragmentation 
        # warning

        i += 49 
        # Allows the function to iterate through the next 49 variables
        # within variable_list

        
    # Converting variable columns to numeric data types:
    for column in variable_list:
        # print(f"Now converting {column} to a numeric type.")
        df_combined_results[column] = pd.to_numeric(
            df_combined_results[column])
        # pd.to_numeric() allows for either integer or float outputs
        # depending on the nature of the original data.
        # See https://pandas.pydata.org/pandas-docs/stable/reference/api/
        # pandas.to_numeric.html

    # Replacing column names with aliases if requested:
    if rename_data_fields == True:
        df_combined_results.rename(
            columns = field_vars_dict, inplace = True)

    # The following for loop moves all of the merge keys (e.g. geographic
    # identifiers) to the left side of the table. This is particularly
    # useful when retrieving longer lists of variables, as otherwise,
    # certain keys can get buried in the middle of the dataset
    for i in range(len(merge_keys)):
        df_combined_results.insert(
            i, merge_keys[i], 
            df_combined_results.pop(merge_keys[i]))

    # Adding a 'Year' column to the left of all existing DataFrame columns:
    # (this will prove particularly
    # helpful when comparing data from different years.)
    df_combined_results.insert(0, 'Year', year)
    
    return df_combined_results

def create_comparison_fields(df, field_var, year_list,
                             field_year_separator = '_'):
    '''This function calculates nominal and percentage changes
    between the last year in a list and all years leading up to that year.
    It also calculates both rank and percentile information for these
    changes.
    
    df: the DataFrame that will be updated with comparisons between years.
    This function assumes that the fields within df that contain 
    data for a particular year use the format
    {field_var}{field_year_separator}{latest_year} (e.g. 'Total_Pop_2009', 
    'Total_Pop_2015', etc.). 
    
    field_var: A string representing the variable 
    whose values should be compared (e.g. 'Total_Pop' within the field
    'Total_Pop_2009'. 

    year_list: A list of years to compare. The function will compare
    all years leading up to the last year with the last year. For example,
    if year_list equals [2005, 2009, 2015], the function will create
    comparisons between (1) 2005 and 2015 and (2) 2009 and 2015 (but not
    2005 and 2009).
    field_var data for each of these years should be stored within
    the DataFrame. For instance, if year_list is equal to the example
    shown above, field_var is 'Total_Pop', and field_year_separator (see
    below) is '_', the script will expect to see the following fields
    within the DataFrame:
    'Total_Pop_2005', 'Total_Pop_2009', 'Total_Pop_2015'

    field_year_separator: The character (e.g. a space, an underscore,
    etc.) separating the field_var and year values within the DataFrame's
    fields.
    
    '''
    latest_year = year_list[-1]
    for year in year_list[:-1]: # E.g. for all years leading up 
        # to (but not including) latest_year

        # Calculating the nominal change between the two years:
        df[f'{year}-{latest_year} {field_var} Change'] = (
        df[f'{field_var}{field_year_separator}{latest_year}'] 
        - df[f'{field_var}{field_year_separator}{year}'] )

        # Calculating the percentage change:
        df[f'{year}-{latest_year} {field_var} % Change'] = 100*((
        df[f'{field_var}{field_year_separator}{latest_year}'] 
        / df[f'{field_var}{field_year_separator}{year}']) - 1)

    
        # Calculating ranks and percentiles for both the nominal 
        # change and % change columns:
        # Note that field_var still needs to be included within these
        # columns in order to specify what change, exactly, is being
        # analyzed. (This is particularly important when this function
        # gets called for multiple field_var entries.)
        df[f'{year}-{latest_year} {field_var} Change Rank'] = df[
        f'{year}-{latest_year} {field_var} Change'].rank(
            ascending=False, method = 'min')
        
        df[f'{year}-{latest_year} {field_var} Change Percentile'] = (
        100 * df[
        f'{year}-{latest_year} {field_var} Change'].rank(
            pct=True, ascending=True, method='max'))
        
        df[f'{year}-{latest_year} {field_var} % Change Rank'] = (
            df[f'{year}-{latest_year} {field_var} % Change'].rank(
            ascending=False, method = 'min'))
        
        df[f'{year}-{latest_year} {field_var} % Change Percentile'] = (
            100 * df[
            f'{year}-{latest_year} {field_var} % Change'].rank(
            pct=True, ascending=True, method='max'))