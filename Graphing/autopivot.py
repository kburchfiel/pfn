def autopivot(df, y, aggfunc, x_vars = [], 
                     color = None, x_vars_to_exclude = [],
                    overall_data_name = 'All Data',
             weight_col = None):
    '''This function will create a pivot table of df that can be used within
    a Plotly graph. It will also return x, y, color, and barmode variables
    that can get incorporated within Plotly charts. (Storing the charting
    code within a separate function makes autopivot more versatile,
    as its output can then be used as the basis for multiple chart types.)

    This function has been designed to work with varying lengths of x_vars
    (i.e. multiple numbers of x variables), including a length of 0. 
    It should therefore prove useful for applications, such as interactive 
    dashboards, that allow the user
    to choose an arbitrary number of comparison variables for a graph.

    df: the DataFrame to use as the basis for the pivot table.
    
    y: the y variable to use within the Plotly graph.
    
    aggfunc: the aggregate function to use within the pivot_table() call
    (e.g. 'mean', 'count', etc.).
    
    x_vars: a list of comparison variables to be converted into 
    an x variable. Pass an empty list in order to group all y values together.
    
    color: the variable that should serve as the color argument for the Plotly
    graph. 

    x_vars_to_exclude: variables that will be incorporated into the pivot table
    (e.g. to ensure it's sorted correctly) but should not be present in the 
    final chart. 
    (For instance, if you've added 'Season' as an x_vars entry or
    color variable, and its values are 'Fall', 'Winter', and 'Spring,' 
    you may also want to add a 'Season For Sorting' column with values of 0, 1, 
    and 2 for Fall, Winter, and Spring, respectively so that they'll 
    appear in chronological order within your chart. These variables should 
    also be placed in x_vars_to_exclude so that they won't make your 
    final graph more complicated and/or cluttered than it needs to be.

    If a variable within x_vars_to_exclude isn't present in your x_vars list
    or your color argument, it will get ignored by the function and thus
    shouldn't cause any issues.
    
    overall_data_name: When x_vars is empty, autopivot will group all
    data into a single row. overall_data_name specifies the name that you 
    would like to give to this data point.    

    weight_col: A column containing group sizes that, if included, will
    be used to calculate weighted averages. (If weight_col is None,
    weighted averages will *not* be calculated.)
    '''

    # Creating a copy of the initial dataset in order to ensure that the 
    # following code does not modify it:
    df_for_pivot = df.copy()
    df_for_pivot

    # Determining which x variables will appear in the final chart:
    x_vars_for_chart = list(set(x_vars) - set(x_vars_to_exclude))
    
    x_var_count = len(x_vars_for_chart)


    if weight_col is not None: # In this case, weighted averages
        # will be calculated.
        # Multiplying each y value by its corresponding weight in order
        # to allow weighted averages to be calculated:
        df_for_pivot[f'{y}_*_{weight_col}'] = (
            df_for_pivot[y] * df_for_pivot[weight_col])
        # These 'y_*_weight' values will get added together during the 
        # pivot table call, as will the corresponding weight column values.
    
    if x_var_count == 0: # Because no comparison variables will appear in
        # the final chart, the function will instead group all data together. 
        # It will do so
        # by creating a new column that has the same value for each row.
        # This column can then serve as the index for the pivot function as well
        # as the color value.
        df_for_pivot[overall_data_name] = overall_data_name

        if weight_col is not None: # In this case, a weighted average
            # of all data within the table will be created.
            df_pivot = df_for_pivot.pivot_table(
            index = overall_data_name, 
                values = [f'{y}_*_{weight_col}', weight_col], 
            aggfunc = 'sum').reset_index()
            # Calculating the weighted average of y by dividing
            # the y_*_weight_col field by its corresponding group size:
            df_pivot[y] = df_pivot[f'{y}_*_{weight_col}'] / df_pivot[weight_col]
        
        else:
            df_pivot = df_for_pivot.pivot_table(
                index = overall_data_name, values = y, 
                aggfunc = aggfunc).reset_index()
        x_val_name = overall_data_name
        color = overall_data_name
        barmode = 'relative'
        index = [overall_data_name] # This value won't be used
        # within autopivot() (defined below), but it will still
        # get created here in order to prevent scripts that expect it to be
        # returned from crashing.
        
       
    else:    
        # If the color variable is also present in x_vars and more than one variable
        # is present within the set of x vars to be charted*, 
        # the graph will display redundant data. Therefore, 
        # the function will remove this variable from x_vars below.
        # (If the only x variable to be charted is also the color variable,
        # we won't want to remove it from x_vars; otherwise, we'd end up with an 
        # empty list of x variables.)
        # *This set (defined above as x_vars_for_chart) excludes any variables
        # also present in x_vars_to_exclude. This will prevent the function
        # from removing a color variable from x_vars that would have been the
        # only variable left in x_vars following the removal of 
        # the variable to exclude (which would cause the function to crash).
        
        # (For example: suppose our color variable were 'Season'; 
        # our x_vars contents were ['Season', 'Season_for_Sorting'];
        # and our x_vars_to_exclude list were ['Season_for_Sorting']. If
        # we chose to remove the color variable from x_vars contents
        # because it contained more than one variable, we'd end up with
        # an empty x_vars list once 'Season_for_Sorting' got removed. Removing
        # this variable to exclude from our list of x vars to pass to len() below
        # will prevent this error.
    
        
        if (color in x_vars) and (len(x_vars_for_chart) > 1):
            x_vars.remove(color)
    
        print("x_vars:",x_vars)
        
        # Initializing a list of variables to be passed to the 'index' argument
        # within the pivot_table call:
        index = x_vars.copy()
        
        # We'll want to make sure to include the color variable in the pivot index
        # as well so that it can be accessed by the charting code.
        if color is not None and color not in index:
            index.append(color)
    
        print("index prior to pivot_table() call:",index)
        

        if weight_col is not None: # In this case, weighted averages
            # will be calculated.
            df_pivot = df_for_pivot.pivot_table(
                index = index, values = [f'{y}_*_{weight_col}', weight_col], 
                aggfunc = 'sum').reset_index()           
            df_pivot[y] = df_pivot[f'{y}_*_{weight_col}'] / df_pivot[weight_col]
            
        else:
            df_pivot = df_for_pivot.pivot_table(
                index = index, values = y, aggfunc = aggfunc).reset_index()
    
        # Now that the pivot table has been created, the variables
        # in x_vars_to_exclude can be removed from our x_vars list, our 
        # index, and our DataFrame, thus preventing our final 
        # graphs from being too cluttered.
        for var_to_exclude in x_vars_to_exclude:
           if var_to_exclude in x_vars:
               x_vars.remove(var_to_exclude)
               index.remove(var_to_exclude)
            # These variables could get removed from df_pivot also,
            # but the user might find them helpful for future sorting needs--
            # so they'll be retained for now.
            # df_pivot.drop(var_to_exclude, axis = 1, inplace = True)

        # Determining the name of the x value column by
        # joining together all of the values in x_vars that will get
        # incorporated into its own values:
        x_val_name = ('/').join(x_vars)

        # Initializing the x_val_name column values (which will serve
        # as the x axis entries within Plotly charts) by 
        # converting the first item within x_vars to a string,
        # then adding other string-formatted values to it:
        # (Slashes will separate these various values.)
        df_pivot[x_val_name] = df_pivot[x_vars[0]].astype('str')
        for i in range(1, len(x_vars)):
            df_pivot[x_val_name] = (
                df_pivot[x_val_name] 
                + '/' + df_pivot[x_vars[i]].astype('str'))
    
        
        # If there are fewer than two unique variables to be graphed, we'll want
        # to set the barmode argument to 'relative' so that, in the event we create
        # a bar chart, the bars won't be far apart from one another. If there are
        # two or more unique variables, we can use 'group' instead.
        # (If there's a single variable within x_vars that matches the 'color' 
        # variable, we will also want to set barmode to 'relative,' since only
        # one variable will actually be displayed on the graph. Therefore, 
        # I added in a set() call in the following code; set() keeps only unique
        # instances of a list and will thus prevent the same x_vars variable
        # and color variable from being counted as two variables within
        # this if/else statement.
        
        if color is not None:
            unique_graphed_vars = set(x_vars + [color])
        else:
            unique_graphed_vars = set(x_vars)
        
        if len(unique_graphed_vars) < 2:
            barmode = 'relative' 
        else:
            barmode = 'group'
    
    return df_pivot, x_val_name, y, color, barmode, x_var_count, index, aggfunc