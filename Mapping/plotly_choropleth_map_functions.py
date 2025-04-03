# Plotly Choropleth Map Functions

import pandas as pd
import geopandas
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def update_and_save_plotly_map(
    fig, filename, static_file_folder='', html_file_folder='', 
    image_extension='png', save_html=True, save_static=True,
    include_plotlyjs='cdn', screenshot_label_font_size=18,
    screenshot_width=1920, screenshot_height=1080,
    screenshot_scale=2, screenshot_title_y=0.95,
    screenshot_title_font_size=40,
    screenshot_colorbar_thickness=80, screenshot_colorbar_len=0.5,
    screenshot_colorbar_tickfont_size=20, 
    screenshot_colorbar_title_font_size=30,
    screenshot_margin_list = None):
    
    '''This function assists with the process of saving a Plotly map as 
    both an HTML file and a static image (if requested). 
    After saving an HTML version of the map, it will then increase the 
    map's width and height so as to increase its relative size; next, it 
    will enlarge certain text and colorbar values accordingly. 
    (These changes are performed in order to adjust for changes in the 
    map's size when it gets converted to a screenshot.) Finally, the 
    function will a static copy of the map.
    
    fig: the map to be saved as an image.

    See the gen_choropleth() documentation within this script for details
    on other arguments.

    '''

    if len(filename) == 0:
        raise ValueError(
            "Please specify a name to assign your map file(s).")
    
    if save_html == True:
        # Adding a forward slash to html_file_folder in order to 
        # distinguish it from the directory: (this step is unnecessary,
        # and will thus be skipped, if html_file_folder is 
        # an empty string.)
        if len(html_file_folder) > 0:
            html_file_folder += '/'
            fig.write_html(html_file_folder + filename + '.html',
                include_plotlyjs=include_plotlyjs)
    if save_static == True:
        fig_for_chart = go.Figure(fig) # This method of creating a copy of
        # the original figure (suggested by StackOverflow user vestland
        # at https://stackoverflow.com/questions/58375026/how-to-make-a-
        # copy-of-a-plotly-figure-object/58375046#58375046)
        # ensures that the following changes won't have any effect on the
        # original figure.
        
        # Adjusting values within the HTML-based map in order to prepare
        # it for conversion to a static image:
        fig_for_chart.update_layout(
            width=screenshot_width, height=screenshot_height, 
            title_font_size=screenshot_title_font_size, 
            title_y=screenshot_title_y)
        fig_for_chart.update_coloraxes(
            colorbar_thickness=screenshot_colorbar_thickness, 
            colorbar_len=screenshot_colorbar_len, 
            colorbar_tickfont_size=screenshot_colorbar_tickfont_size,
            colorbar_title_font_size=screenshot_colorbar_title_font_size)
        
        if screenshot_margin_list is not None:
            fig_for_chart.update_layout(margin = {
                "r":screenshot_margin_list[0],
                "t":screenshot_margin_list[1],
                "l":screenshot_margin_list[2],
                "b":screenshot_margin_list[3]})

        # Data labels may be stored either as scattermaps or scattergeos,
        # so the following lines include commands for both label types.
        fig_for_chart.update_traces(
            textfont_size=screenshot_label_font_size,
            selector=dict(type='scattermap'))
        
        
        fig_for_chart.update_traces(
            textfont_size=screenshot_label_font_size, 
            selector=dict(type='scattergeo'))
        # The above line is based on the documentation found in 
        # https://plotly.com/python/reference/scattergeo/ .
        
        if len(static_file_folder) > 0:
            static_file_folder += '/'
        fig_for_chart.write_image(
            file=static_file_folder + filename + '.' + image_extension, 
            width=screenshot_width, height=screenshot_height, 
            scale=screenshot_scale)


def pre_map(original_gdf, data_col, geojson_col, location_name_col, 
            colormap_type, data_round_value, extra_hover_cols, 
            colorscale_tick_count=10, tick_round_value=2, 
            percentile_round_value=2):
    '''
    This function is called by gen_choropleth() and gen_choropleth_map()
    in order to prepare the dataset for mapping. It also calculates values
    for percentile-based bins that those functions can use.
    See the gen_choropleth() documentation within this script for details
    on this function's arguments.
    '''
    
    # Creating a copy of the original DataFrame (so as not to modify
    # it):
    # This copy will also be sorted by the data column in descending 
    # order. This step helps ensure that, when a percentile-based 
    # colorbar is requested, the colorbar legend entries (which are 
    # retrieved from the sort_list variable created within this function)
    # will appear within the same order as the percentile_quantile_list
    # values. The latter are sorted explicitly within the function,
    # but the former are not--so sorting the DataFrame at the outset
    # helps keep them synchronized.
    # In addition, this code will set the DataFrame's index as 
    # location_name_col. This ensures that this column, rather than
    # the existing index, will be used as the basis of choropleth
    # region names--thus preventing incorrect/unexpected output.
    # This code will also remove any rows with missing data_col() values
    # and remove columns that aren't needed for the map. (The latter step
    # may help the script run a bit faster and will also help avoid naming 
    # conflicts when new columns are created.)

    # Determining which columns to retain within this DataFrame:
    # (Removing unnecessary columns 
    cols_to_keep = (
        [data_col, location_name_col, geojson_col] + extra_hover_cols)
        
    gdf = original_gdf[cols_to_keep].copy().dropna(
        subset = data_col).sort_values(data_col, ascending=False)
    gdf.set_index(location_name_col, inplace=True)
    # The previous code could be preceded by the following check
    # (to account for cases in which the index already contains
    # location_name_col values):
    # if gdf.index.name != location_name_col:

    
    # Creating a column that shows each value's percentile rank:
    # (Although these will be particularly useful for choropleth
    # maps whose colors are based on the percentiles of each value,
    # they may also be of interest within other maps--so I updated this
    # function to run the following code for all colormap_type values.
    percentile_col = data_col+' (Percentile)'
    if percentile_col in gdf.columns: # This is less likely to return True
        # now that the DataFrame has been filtered to include only those
        # columns in cols_to_keep.
        raise ValueError(f"The name of the column that will be used \
to store data_col percentiles ({percentile_col}) is already present \
within gdf. Rename this column before calling the function to prevent \
any conflicts.")   

    gdf[percentile_col] = 100 * gdf[
    data_col].rank(pct=True, ascending=True, method='max') # See
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/
    # pandas.DataFrame.rank.html
    # for more information on the use of df.rank() to create
    # percentile ranks.


    if colormap_type == 'percentile':
        # In order to accommodate percentile-based color ranges, 
        # the following code will create lists of selected
        # percentile ranks along with their corresponding data_col values.
        # These rank and value lists will then be passed to the
        # colorbar_tickvals and colorbar_ticktext arguments
        # of an update_coloraxes() call. This will allow maps that feature
        # percentile-based colors to still show to show actual values 
        # within their legends.

        quantile_increment = 1/(colorscale_tick_count - 1) 
        # This variable will determine
        # the distance between increments within np.arange(), 
        # which we'll call below in order to determine which 
        # quantiles to retrieve from the DataFrame.
        # I subtracted 1 from the denominator so that the final number of
        # quantiles (which will include both a minimum and maximum value)
        # will match the 'quantile quantity' specified within 
        # tick_count.

        # Using quantile_increment to specify which quantiles to retrieve:

        # quantile_range will increase from 0 to 1 by the amount 
        # specified in quantile_increment. `quantile_increment/2` 
        # is added to 1 in the function call in order to ensure that 
        # the output will include, but also stop at, 1.

        quantile_range = np.arange(0, 1+quantile_increment/2, 
                           quantile_increment)
        
        # The 'lower' interpretation method will help ensure that only 
        # actual percentile ranks present in the DataFrame get retrieved.
        # This is a necessary prerequisite for using df.query() to 
        # locate the scores that match these percentile ranks, 
        # which we'll do shortly.

        # Finding the actual percentile ranks within our DataFrame 
        # that correspond to these quantiles:

        # (A quantile of 0 refers to the smallest percentile rank in the 
        # dataset, while a quantile of 1 refers to the highest percentile 
        # rank; a quantile of 0.5, if specified, refers to the median 
        # percentile rank.)
        
        # Note: in an earlier version of this code, I created revised 
        # colorbars using the following steps:
        
        # 1. I used quantile() to figure out which data column values to 
        # pass to the colorbar's 'ticktext' property.
        # 2. I then multiplied quantile_range() by 100 to create a range 
        # of percentile ranks (called `percentile_range`) that could be 
        # passed to the colorbar's 'tickvals' property.
          
        # However, this approach had a significant flaw: because datasets 
        # often wouldn't have an exact copy of one of the percentile ranks 
        # in percentile_range, the scores that replaced those 
        # percentile ranks often corresponded to a slightly different 
        # percentile rank. (In one actual example, Pandas calculated 
        # the quantile of 0.5 (e.g. the 50.000th percentile) as 6.289%, 
        # but this percentage actually represented the 50.98th percentile. 
        # It would therefore be inaccurate to replace the 50th-percentile 
        # marker in the colorbar with this value.)
        
        # In order to avoid this issue, I revised the code so that it 
        # would find the quantiles of the actual *percentile ranks* in 
        # our dataset. This way, all of the percentile ranks passed to 
        # the colorbar's tickvals property would have actual corresponding 
        # values that could be passed to colorbar_ticktext.

        # This sort_values() call is necessary for the quantile
        # ranges to line up with the score_list values that will
        # get created shortly.
        # I also added in 'lower' as my interpolation argument
        # so that each quantile would be an actual data point 
        # rather than an approximation.
        percentile_quantiles = gdf[percentile_col].quantile(
        quantile_range, interpolation='lower').sort_values(
        ascending=False)

        percentile_quantile_list = percentile_quantiles.to_list()

        # Determining the actual data_col values within the dataset 
        # that correspond to these percentile ranks:

        # Note that only one row will be retained for each percentile rank; 
        # this will ensure that the lengths of the percentile rank and 
        # percentile score lists match. (If these lengths differed, we 
        # could encounter issues when trying to replace the former with 
        # the latter within our colorbar.)

        percentile_rank_score_pairs = gdf.query(
            f"`{percentile_col}` in @percentile_quantile_list"
        ).drop_duplicates(percentile_col).copy()
        
        score_series = percentile_rank_score_pairs[data_col]
        if tick_round_value is not None:
            score_series = score_series.round(tick_round_value)
        score_list = score_series.to_list()
               
        color = percentile_col # Setting percentile_col as the color
        # argument will allow for a wider diversity of colors in the 
        # event that outliers exist within the dataset.
    else:
        color = data_col # The data column values will be mapped
        # to color values in a linear fashion
        # Initializing the following variables at None so that
        # the same number of variables will get returned by the function
        # regardless of colormap_type's value
        score_list = None
        percentile_quantile_list = None


    # Specifying hover_data values:
    # These values will take the data_round_value and 
    # percentile_round_value arguments into account.
    # Note that the percentile column can be identified as 
    # the data_col value + ' (Percentile').
    hover_data = {data_col:f':.{data_round_value}f',
    data_col + ' (Percentile)':f':.{percentile_round_value}f'}
    # Adding the values in extra_hover_col to this list:
    hover_data.update({col:True for col in extra_hover_cols})

    return gdf, score_list, color, percentile_quantile_list, hover_data
    

def post_map(fig, gdf, margin_list, colorbar_len, colormap_type,
            custom_colorbar_title, data_col,
            percentile_quantile_list, score_list, add_labels,
            label_round_value, revise_state_label_points,
            label_addition_method):

    '''
    This function is called by gen_choropleth() and gen_choropleth_map()
    in order to make modifications to choropleth maps that were initialized
    within those functions.
    See the gen_choropleth() documentation within this script for details
    on this function's arguments.
    '''    
    
    # (The following code is based on a snippet from
        # https://plotly.com/python/map-configuration/ 
    if margin_list is not None:
        fig.update_layout(margin = {
            "r":margin_list[0],"t":margin_list[1],
            "l":margin_list[2],"b":margin_list[3]})
    fig.update_layout(coloraxis_colorbar_len = colorbar_len)
    
    if colormap_type == 'percentile':
    # The following code updates the figure's colorbar to show the values 
    # corresponding to each percentile rather than the percentiles 
    # themselves. It does so by (1) 
    # selecting the percentile quantiles calculated earlier 
    # as the colorbar tick locations; (2) selecting these quantiles' 
    # corresponding percentile scores as the colorbar values; 
    # and (3) changing the title of the colorbar to reflect
    # the data being displayed within the tick text entries.

        if custom_colorbar_title is not None:
            colorbar_title = custom_colorbar_title
        else:
            colorbar_title = data_col

    # The documentation at 
    # https://plotly.com/python/reference/layout/coloraxis/
    # proved indispensable in drafting this code.
        
        fig.update_coloraxes(
            colorbar_tickvals=percentile_quantile_list,
            colorbar_tickmode='array',
            colorbar_ticktext=score_list,
            colorbar_title=colorbar_title,
            colorbar_title_side='bottom')

    # I chose to set colorbar_title_side as 'bottom' because it ended up 
    # pretty close to the topmost tick when the default setting 
    # ('top') was used.)

    if add_labels == True:
        label_col = data_col+'_for_labels'
        if label_col in gdf.columns:
            raise ValueError(f"The name of the column that will be used \
to store text labels ({label_col}) is already present \
within gdf. Rename this column before calling the function to prevent \
any conflicts.")   
        # The function assumes that the caller wishes to plot data_col
        # values as text labels; however, it could be revised
        # to allow for an alternative set of labels.
        gdf[label_col] = gdf[data_col].copy()
        if label_round_value is not None:
            gdf[label_col] = gdf[label_col].round(label_round_value)
        # Now that the label column has been rounded, it should be 
        # converted to a string; otherwise, the labels may not appear
        # correctly (depending on what function is being used to 
        # add them).
        gdf[label_col] = gdf[label_col].astype('str')
    
        # Determining points within each region that can serve as 
        # text label locations:
        # (See https://geopandas.org/en/stable/docs/reference/
        # api/geopandas.GeoSeries.representative_point.html
        # for more infomation.)
        for column in ['label_loc', 'label_lat', 'label_lon']:
            if column in gdf.columns:
                raise ValueError(f"Rename the column {column} in order \
to prevent a conflict with gen_choropleth.")
        gdf['label_loc'] = gdf['geometry'].representative_point()
        # Adding the x and y coordinates stored within label_loc to
        # standalone fields for use within Plotly's 
        # add_scattergeo() function:
        gdf['label_lat'] = [coord.y for coord in gdf['label_loc']]
        gdf['label_lon'] = [coord.x for coord in gdf['label_loc']]

        if revise_state_label_points == True:
            # Shifting data labels to make them easier to locate
            # and read:
            # (These points were determined using Openstreetmap 
            # coordinates as a reference.)
            gdf.at['Maryland', 'label_lat'] = 39.5
            gdf.at['Maryland', 'label_lon'] = -77.17
            
            gdf.at['Michigan', 'label_lat'] = 43.63
            gdf.at['Michigan', 'label_lon'] = -84.97
            
            gdf.at['Louisiana', 'label_lat'] = 30.5
            gdf.at['Louisiana', 'label_lon'] = -92.54

        # Adding labels to the map using the function specified by
        # label_addition_method:
        
        if label_addition_method == 'scattergeo':
            # This code was based mostly on
            # https://plotly.com/python/scatter-plots-on-
            # maps/#simple-us-airports-map .
    
            fig.add_scattergeo(
                text=gdf[label_col],
                mode='text',
                lat=gdf['label_lat'],
                lon=gdf['label_lon'])
            # The following code for disabling hover labels (so that
            # they don't interfere with existing hover values) 
            # was based on:
            # https://plotly.com/python/reference/scattergeo/ 
            fig.update_traces(hoverinfo = 'skip', selector = dict(
                type='scattergeo'))
        
        elif label_addition_method == 'scattermap':

            fig.add_traces(go.Scattermap(
                text=gdf[label_col],
                lat=gdf['label_lat'],
                lon=gdf['label_lon'],
                mode='text',
                hoverinfo='skip',
                showlegend=False,
                ))
            # This add_traces() call is based on a response by
            # r-beginners at 
            # https://community.plotly.com/t/is-it-possible-to-use-add-
            # scattergeo-to-add-text-labels-to-a-map-created-with-px-
            # choropleth-map-not-px-choropleth/91543/2 .
            
            # The hoverinfo = 'skip' code came from the scattermap 
            # documentation at:
            # https://plotly.com/python/reference/scattermap/

            # I also tried out the following method, which worked
            # fairly well--except that hover data for these labels
            # continued to appear (thus interfering with users' ability
            # to view other hover tooltips).
            
            # fig.add_traces(px.scatter_map(
            #     gdf,
            #     text=label_col,
            #     lat='label_lat',
            #     lon='label_lon',
            #     map_style = 'white-bg',
            #     ).update_traces(
            #     mode='text', marker_allowoverlap=True, hovertext='', 
            #     hoverinfo='skip').data)
            
            # This method of adding a Plotly figure to an existing
            # figure comes from StackOverflow user montol at
            # https://stackoverflow.com/a/77888204/13097194 .

            # It is meant to prevent these labels from appearing when the
            # user hovers over them (as that can be distracting). However,
            # this update doesn't appear to have an effect on the 
            # actual map. 

        else:
            raise ValueError("Unrecognized label_addition_method passed \
            to function.")
        
        
    
def gen_choropleth(
    original_gdf, geojson_col, data_col, location_name_col,
    extra_hover_cols=[], color_continuous_scale=None, 
    scope=None, title=None, basemap_visible=False, 
    colormap_type='linear', colorscale_tick_count=10, 
    tick_round_value=None, custom_colorbar_title=None, add_labels=False, 
    label_round_value=2, label_addition_method='scattergeo',
    percentile_round_value=2, data_round_value=2,
    save_html=True, save_static=True, static_file_folder='',
    html_file_folder='', filename='', image_extension='png',
    include_plotlyjs='cdn', screenshot_label_font_size=18,
    screenshot_width=1920, screenshot_height=1080,
    screenshot_scale=2, screenshot_title_y=0.95,
    screenshot_title_font_size=40, screenshot_colorbar_thickness=80, 
    screenshot_colorbar_len=0.5, screenshot_colorbar_tickfont_size=20, 
    screenshot_colorbar_title_font_size=30, screenshot_margin_list=None,
    revise_state_label_points=False, debug=False, 
    margin_list=None, colorbar_len=1):
    
    '''
    This function converts a GeoDataFrame into a choropleth map within 
    Plotly, then saves that map (if requested by the caller) to HTML and 
    image files. It also allows for percentile-based color ranges 
    (which can better display data that contains outliers).
    
    Note: this function assumes that the values to be passed to the 
    choropleth map exist within the GeoDataFrame's index.

    Make sure to consult the documentation for px.choropleth()
    available at 
    (https://plotly.com/python-api-reference/generated/plotly.
    express.choropleth.html)
    as needed.
    
    original_gdf: the GeoDataFrame from which regional boundaries 
    and data will be retrieved. (The function will create a copy of this
    DataFrame so as not to modify it.)

    geojson_col: the column within gdf that contains boundary data. This
    will be passed to the geojson argument of px.choropleth().

    data_col: the column within gdf that contains data to be mapped.

    location_name_col: A column storing location names (e.g. state
    names, county names, etc). The location names within this column
    will appear as hover values within the interactive map produced
    by this script.

    extra_hover_cols: A list of columns *in addition to* data_col that 
    should be displayed when the user hovers over a given region.

    color_continuous_scale: A custom color scale to pass to the 
    color_continuous_scale parameter of px.choropleth().

    scope: the argument (e.g. 'usa') to pass to the 'scope' parameter
    of px.choropleth().

    title: the title to use for the map.

    basemap_visible: set to True to render the Plotly basemap and False
    to exclued it.

    colormap_type: set to 'percentile' in order to render map colors
    based on the *percentile ranks* of data_col values. Set to *linear*
    in order to base these colors directly on data_col values. Although
    both the region colors and colorbar color scale will reflect
    percentile ranks, the colorbar text entries will still show actual
    data_col values.

    colorscale_tick_count: The number of ticks (and, in turn, text entries)
    to include within the map's colorbar. (Currently, this argument will 
    only get applied if colormap_type is set to 'percentile.')

    tick_round_value: The value to pass to round() when rounding colorbar
    text entries. Set this value to 0 for integers, 1 for single 
    decimal points, 2 for two decimal points, and so on.
    Set to None to prevent these entries from getting rounded. If 
    colormap_type is not set to 'percentile', this argument will have
    no effect.

    custom_colorbar_title: A custom title to use for the colorbar. 
    If None is used as its argument, data_col will be used as the 
    colorbar title by default. If colormap_type is not set to 'percentile', 
    this argument will have no effect.

    add_labels: set to True to add text labels to the map.

    label_round_value: The value to pass to round() when rounding text
    labels on the map (and not legend labels--whose rounding is governed
    by tick_round_value).
    Set this value to 0 for integers, 1 for single 
    decimal points, 2 for two decimal points, and so on.
    Set to None to prevent these entries from getting rounded.

    label_addition_method: Set to 'scattergeo' to use add_scattergeo()
    to add labels to maps; set to set to 'scattermap' to use 
    go.scattermap() instead. (The former works great for the 
    non-tiled maps that gen_choropleth() creates; the latter appears 
    to work better for tiled maps generated within px.choropleth_map()).
 
    percentile_round_value: The value to pass to round() when creating 
    rounded copies of percentile data (thus improving the appearance of
    these percentiles within the interactive map's tooltips). Set to 
    None to prevent these percentiles from getting rounded.

    data_round_value: The value to pass to round() when creating 
    rounded copies of data_col values (thus improving the appearance of
    these values within the interactive map's tooltips). Set to 
    None to use unrounded values instead.

    revise_state_label_points: set to True to shift the data label 
    locations for Maryland; (so as not to overlap with DC's); 
    Michigan (so that it appears within the 'hand' rather than the 
    'peninsula'); and Louisiana (to move it off of the Mississippi border). 
    These operations will only work if you're creating labels
    for US states and have 'Maryland', 'Michigan', and 'Louisiana' 
    as index entries.

    static_file_folder and html_file_folder: The folder paths 
    (either relative or absolute) in which to save static and interactive 
    copies of the map, respectively. These paths should not include the 
    desired filename, as that will get added in via the filename argument. 
    In addition, they should not include any trailing forward or 
    backward slashes.

    filename: The name to use when saving the file. This name should 
    include the file name but *not* any image extensions; these will get 
    added in manually.
    
    image_extension: the image extension (e.g. 'png', 'svg', etc) to use 
    when saving a static copy of the map.

    save_html and save_static: set to True to save HTML-based and static
    copies of the map, respectively.

    margin_list: The right, top, left, and bottom margins to use for
    the map, respectively. 

    include_plotlyjs: The argument to pass to the respective 
    include_plotlyjs parameter within write_html(). The default setting
    allows for smaller HTML file sizes; however, if it's important for
    your maps to render offline, select True as your argument instead.
    For more details on these and other options, consult 
    https://plotly.com/python-api-reference/generated/
    plotly.io.write_html.html .

    screenshot_label_font_size: The font size in which data labels
    should appear within the screenshot.

    screenshot_width and screenshot_height: The values to pass to the
    width and height arguments, respectively, of an update_layout()
    call.

    screenshot_scale: The scale to use when saving a static copy of the
    map. NOTE: the actual dimensions of the map will equal 
    screenshot_width * scale and screenshot_height * scale. You can 
    tweak these values as needed so that your screenshot has a 
    sufficiently high resolution but remains readable.

    screenshot_title_y and screenshot_title_font_size: Arguments for
    tweaking the screenshot title's vertical location and font size,
    respectively.
  
    screenshot_colorbar_thickness, screenshot_colorbar_len,
    screenshot_colorbar_tickfont_size, and 
    screenshot_colorbar_title_font_size: Arguments for modifying the
    thickness, length, tick font size, and title font size, 
    respectively, of the screenshot's colorbar.  

    screenshot_margin_list: Similar to margin_list, except that these 
    values will govern the margins of the copy of the map that will
    be saved as a screenshot.

    debug: set to True to return both the figure and additional variables
    that can help with troubleshooting or extending the function; 
    set to False to return just the figure.

    coloraxis_colorbar_len: The length to use for colorbars. 
    '''

    # Creating a modified copy of the dataset for mapping purposes and
    # calculating other relevant values that will get incorporated
    # into the map:
    gdf, score_list, color, percentile_quantile_list, hover_data = pre_map(
        original_gdf=original_gdf, data_col=data_col, 
        geojson_col=geojson_col, location_name_col=location_name_col, 
        colormap_type=colormap_type,
        colorscale_tick_count=colorscale_tick_count,
        tick_round_value=tick_round_value, 
        data_round_value=data_round_value, 
        extra_hover_cols=extra_hover_cols)

    # Generating a choropleth map:
    # Note that we need to use geojson=gdf[geojson_col] here
    # rather than just geojson=geojson_col.
    fig = px.choropleth(gdf, geojson=gdf[geojson_col],
    locations=gdf.index, color=color, hover_data=hover_data,
    color_continuous_scale=color_continuous_scale,
    scope=scope, title=title, basemap_visible=basemap_visible)

    # Performing additional updates to this map:
    post_map(fig=fig, gdf=gdf, margin_list=margin_list, 
             colorbar_len=colorbar_len, colormap_type=colormap_type,
            custom_colorbar_title=custom_colorbar_title, 
            data_col=data_col, label_addition_method=label_addition_method,
            percentile_quantile_list=percentile_quantile_list, 
            score_list=score_list, add_labels=add_labels,
            label_round_value=label_round_value, 
             revise_state_label_points=revise_state_label_points)       


    # Saving this map to HTML and static files 
    # (if requested by the caller):
    if (save_html == True) or (save_static == True):
        update_and_save_plotly_map(
            fig=fig, save_html=save_html, save_static=save_static, 
            static_file_folder=static_file_folder,
            html_file_folder=html_file_folder, filename=filename, 
            image_extension=image_extension, 
            include_plotlyjs=include_plotlyjs, 
            screenshot_label_font_size=screenshot_label_font_size,
            screenshot_width=screenshot_width, 
            screenshot_height=screenshot_height,
            screenshot_scale=screenshot_scale, 
            screenshot_title_y=screenshot_title_y,
            screenshot_title_font_size=screenshot_title_font_size, 
            screenshot_colorbar_thickness=screenshot_colorbar_thickness, 
            screenshot_colorbar_len=screenshot_colorbar_len, 
            screenshot_colorbar_tickfont_size=\
            screenshot_colorbar_tickfont_size, 
            screenshot_colorbar_title_font_size=\
            screenshot_colorbar_title_font_size,
            screenshot_margin_list=screenshot_margin_list)
        
    if debug == True:
        return fig, percentile_quantile_list, score_list, gdf
    else:
        return fig  

def gen_choropleth_map(
    original_gdf, geojson_col, data_col, location_name_col,
    extra_hover_cols=[], color_continuous_scale=None, title=None,
    colormap_type='linear', 
    colorscale_tick_count=10, tick_round_value=None,
    custom_colorbar_title=None, add_labels=False, 
    label_round_value=2, label_addition_method='scattermap',
    percentile_round_value=2, data_round_value=2,
    save_html=True, save_static=True, static_file_folder='',
    html_file_folder='', filename='', image_extension='png',
    include_plotlyjs='cdn', screenshot_label_font_size=30,
    screenshot_width=3840, screenshot_height=2160,
    screenshot_scale=1, screenshot_title_y=0.95,
    screenshot_title_font_size=70, screenshot_colorbar_thickness=80, 
    screenshot_colorbar_len=0.5, screenshot_colorbar_tickfont_size=40, 
    screenshot_colorbar_title_font_size=50, screenshot_margin_list=[
        0, 200, 0, 0],
    revise_state_label_points=False, debug=False, 
    colorbar_len=0.8, margin_list=[0, 0, 0, 0],
    tile_source='open-street-map', zoom=4.35, 
    starting_loc=[37.9, -96], opacity=0.75):
    
    '''
    This function is similar to gen_choropleth() except that it renders
    to maps using px.choropleth_map(),
    thus allowing tiles to appear behind the map, rather than 
    px.choropleth(). Both options have their 
    strengths and weaknesses for various use cases.
    For more on choropleth_map(), see 
    https://plotly.com/python-api-reference/generated/
    # plotly.express.choropleth_map.html .

    The gen_choropleth() docstring contains details for most of the 
    parameters defined in this function. Parameters unique to this function
    are described below:
    
    tile_source: The map tile provider to use.

    zoom: The starting zoom to use for a map. 

    starting_loc: A list of floats representing the starting latitude
    and longitude for the map. These should be represented in decimal
    degree format rather than degrees/minutes/seconds format. 

    (Note: the default zoom and starting_loc settings are tailored towards
    HTML-resolution maps of the lower 48 US states.)

    opacity: The opacity level to use for choropleth regions. 

    Notes on differences in default arguments between gen_choropleth_map()
    and gen_choropleth():   
    
    1. a colorbar_len entry of 0.8 will shorten the colorbar 
    a little so that the reduced bottom margin does not cut off the 
    legend's title. (This code was derived from
    https://plotly.com/python/reference/layout/coloraxis/ .)

    2. Setting each value within margin_list to 0 will allow the map to 
    take up more of the window--which can be particularly useful for 
    tiled maps. (This approach is based on a snippet from
    https://plotly.com/python/map-configuration/ .)

    3. screenshot_margin_list, however, uses values of [0, 200, 0, 0]
    in order to allow for more space for a title.  

    4. The screenshot_width and screenshot_height settings are
    3840 and 2160, respectively, because I found that static tiled maps 
    appear clearer when higher width and height settings are applied.

    5. Font sizes have also been increased in order to better fit these
    larger width and height settings.

    NOTE: If you set add_labels to True, you may get an error message
    when attempting to save the map as a PNG file via
    update_and_save_plotly_map() (which this function calls). Thus, if you 
    don't need a static copy of your map, I recommend setting save_static
    to False. If you *do* need a static copy, consider using
    gen_choropleth() instead (as that function can save PNG versions of
    labeled maps without any trouble); taking a screenshot manually;
    or using Selenium to automate the screenshot generation process.
    
    '''

    gdf, score_list, color, percentile_quantile_list, hover_data = pre_map(
        original_gdf=original_gdf, data_col=data_col, 
        geojson_col=geojson_col, location_name_col=location_name_col, 
        colormap_type=colormap_type,
        colorscale_tick_count=colorscale_tick_count,
        tick_round_value=tick_round_value, 
        data_round_value=data_round_value, 
        extra_hover_cols=extra_hover_cols)

    # Generating a tiled choropleth map:   
    fig = px.choropleth_map(gdf, geojson=gdf[geojson_col],
    locations=gdf.index, color=color, hover_data = hover_data,
    color_continuous_scale=color_continuous_scale,
    title=title, map_style=tile_source, zoom=zoom,
    center={'lat':starting_loc[0], 'lon':starting_loc[1]},
    opacity=opacity)

    post_map(fig=fig, gdf=gdf, margin_list=margin_list, 
            colorbar_len=colorbar_len, colormap_type=colormap_type,
            custom_colorbar_title=custom_colorbar_title, 
            data_col=data_col, label_addition_method=label_addition_method,
            percentile_quantile_list=percentile_quantile_list, 
            score_list=score_list, add_labels=add_labels,
            label_round_value=label_round_value, 
            revise_state_label_points=revise_state_label_points)       

    if (save_html == True) or (save_static == True):
        update_and_save_plotly_map(
            fig=fig, save_html=save_html, save_static=save_static, 
            static_file_folder=static_file_folder,
            html_file_folder=html_file_folder, filename=filename, 
            image_extension=image_extension, 
            include_plotlyjs=include_plotlyjs, 
            screenshot_label_font_size=screenshot_label_font_size,
            screenshot_width=screenshot_width, 
            screenshot_height=screenshot_height,
            screenshot_scale=screenshot_scale, 
            screenshot_title_y=screenshot_title_y,
            screenshot_title_font_size=screenshot_title_font_size, 
            screenshot_colorbar_thickness=screenshot_colorbar_thickness, 
            screenshot_colorbar_len=screenshot_colorbar_len, 
            screenshot_colorbar_tickfont_size=\
            screenshot_colorbar_tickfont_size, 
            screenshot_colorbar_title_font_size=\
            screenshot_colorbar_title_font_size,
            screenshot_margin_list=screenshot_margin_list)
        
    if debug == True:
        return fig, percentile_quantile_list, score_list, gdf
    else:
        return fig