# Plotly Choropleth Map Functions

# By Kenneth Burchfiel

# Released under the MIT License

import pandas as pd
import geopandas
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def update_and_save_plotly_map(
    fig, filename, static_file_folder = '', html_file_folder = '', 
    image_extension = 'png', save_html = True, save_static = True,
    include_plotlyjs = 'cdn', screenshot_label_font_size = 18,
    screenshot_width = 1920, screenshot_height = 1080,
    screenshot_scale = 2, screenshot_title_y = 0.95,
    screenshot_title_font_size = 40,
    screenshot_colorbar_thickness = 80, screenshot_colorbar_len = 0.5,
    screenshot_colorbar_tickfont_size = 20, 
    screenshot_colorbar_title_font_size = 30):
    
    '''This function assists with the process of saving a Plotly map as 
    both an HTML file and a static image (if requested). 
    After saving an HTML version of the map, it will then increase the 
    map's width and height so as to increase its relative size; next, it 
    will enlarge certain text and colorbar values accordingly. 
    (These changes are performed in order to adjust for changes in the 
    map's size when it gets converted to a screenshot.) Finally, the 
    function will a static copy of the map.
    
    fig: the map to be saved as an image.
    
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
    sufficiently high resoultion but remains readable.

    screenshot_title_y and screenshot_title_font_size: Arguments for
    tweaking the screenshot title's vertical location and font size,
    respectively.
  
    screenshot_colorbar_thickness, screenshot_colorbar_len,
    screenshot_colorbar_tickfont_size, and 
    screenshot_colorbar_title_font_size: Arguments for modifying the
    thickness, length, tick font size, and title font size, 
    respectively, of the screenshot's colorbar.  
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
                include_plotlyjs = include_plotlyjs)
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
            width = screenshot_width, height = screenshot_height, 
            title_font_size = screenshot_title_font_size, 
            title_y = screenshot_title_y)
        fig_for_chart.update_coloraxes(
            colorbar_thickness = screenshot_colorbar_thickness, 
            colorbar_len = screenshot_colorbar_len, 
            colorbar_tickfont_size = screenshot_colorbar_tickfont_size,
            colorbar_title_font_size = screenshot_colorbar_title_font_size)
        fig_for_chart.update_traces(
            textfont_size=screenshot_label_font_size, 
            selector=dict(type='scattergeo'))
        # The above line is based on the documentation found in 
        # https://plotly.com/python/reference/scattergeo/ .
        
        if len(static_file_folder) > 0:
            static_file_folder += '/'
        fig_for_chart.write_image(
            file = static_file_folder + filename + '.' + image_extension, 
            width = screenshot_width, height = screenshot_height, 
            scale = screenshot_scale)

def gen_choropleth(
    original_gdf, geojson_col, data_col, extra_hover_cols = [], 
    color_continuous_scale=None, scope=None, title=None,
    basemap_visible=False, colormap_type='linear', 
    colorscale_tick_count=10, tick_round_value=None,
    custom_colorbar_title=None, add_labels=False, 
    label_round_value=None,
    save_html=True, save_static=True, static_file_folder='',
    html_file_folder='', filename='', image_extension='png',
    include_plotlyjs='cdn', screenshot_label_font_size=18,
    screenshot_width=1920, screenshot_height=1080,
    screenshot_scale=2, screenshot_title_y=0.95,
    screenshot_title_font_size=40, screenshot_colorbar_thickness=80, 
    screenshot_colorbar_len=0.5, screenshot_colorbar_tickfont_size=20, 
    screenshot_colorbar_title_font_size=30,
    revise_state_label_points=False, debug=False, show_tiles=False,
    tile_source='open-street-map', zoom=4.35, 
    starting_loc=[37.9, -96],
    opacity=0.75, margin_list=None, colorbar_len=-1):
    
    '''This function converts a GeoDataFrame into a choropleth map within 
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

    label_round_value: The value to pass to round() when rounding labels. 
    Set this value to 0 for integers, 1 for single 
    decimal points, 2 for two decimal points, and so on.
    Set to None to prevent these entries from getting rounded.

    revise_state_label_points: set to True to shift the data label 
    locations for Maryland; (so as not to overlap with DC's); 
    Michigan (so that it appears within the 'hand' rather than the 
    'peninsula'); and Louisana (to move it off of the Mississippi border). 
    These operations will only work if you're creating labels
    for US states and have 'Maryland', 'Michigan', and 'Louisiana' 
    as index entries.

    save_html and subsequent arguments will get passed to their equivalent 
    arguments within update_and_save_plotly_map(); 
    see that function's documentation for further details on these
    entries.

    debug: set to True to return both the figure and additional variables
    that can help with troubleshooting or extending the function; 
    set to False to return just the figure.

    show_tiles: Set to True to render the map using px.choropleth_map(),
    thus allowing tiles to appear behind the map. Keep False to render
    the map using px.choropleth() instead. Both options have their 
    strengths and weaknesses for various use cases.
    For more on choropleth_map(), see https://plotly.com/python-api-reference/generated/plotly.express.choropleth_map.html .

    tile_source: The map tile provider to use. (Will only have an effect
    if show_tiles is set to True.)

    zoom: The starting zoom to use for a map. (Will only have an effect
    if show_tiles is set to True.) 

    starting_loc: A list of floats representing the starting latitude
    and longitude for the map. These should be represented in decimal
    degree format rather than degrees/minutes/seconds format. (Will only 
    have an effect if show_tiles is set to True.)

    (Note: the default zoom and starting_loc settings are tailored towards
    HTML-resolution maps of the lower 48 US states.)

    opacity: The opacity level to use for choropleth regions. It will only
    have an effect if show_tiles is set to True.

    margin_list: The right, top, left, and bottom margins to use for
    the map, respectively. If set to None, the map's default margins
    will be retained if show_tiles is False but set to 0 on all sides
    if show_tiles is True.

    coloraxis_colorbar_len: The length to use for colorbars. If set
    to -1, this value will get changed within the function to 1 (if
    show_tiles is False) or 0.8 (if show_tiles is True). (A smaller
    colorbar can help prevent its title from getting cut off when the
    bottom margin is removed--which will occur by default when show_tiles
    is set to True.)
    
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
    
    gdf = original_gdf.copy().sort_values(data_col, ascending = False)

    if colormap_type == 'percentile':
        # In order to accommodate percentile-based color ranges, 
        # the following code will (1) generate percentile ranks
        # for the values in data_col, then (2) create lists of selected
        # ranks along with their corresponding data_col values.
        # These rank and value lists will then be passed to the
        # colorbar_tickvals and colorbar_ticktext arguments
        # of an update_coloraxes() call.
    
        percentile_col = data_col+'_percentiles_for_map'
        if percentile_col in gdf.columns:
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
        percentile_quantiles = gdf[percentile_col].quantile(
        quantile_range, interpolation = 'lower').sort_values(
        ascending = False)

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
        # argument will allow fdor a wider diversity of colors in the 
        # event that outliers exist within the dataset.
    else:
        color = data_col
    if show_tiles == False: # px.choropleth() will be called
        # to produce a tileless choropleth map.
        if colorbar_len == -1:
            colorbar_len = 1
        fig = px.choropleth(gdf, 
        geojson=gdf[geojson_col],
        locations=gdf.index,
        color=color,
        hover_data=[data_col] + extra_hover_cols, 
        color_continuous_scale=color_continuous_scale,
        scope=scope,
        title=title,
        basemap_visible = basemap_visible)

    else: # px.choropleth_map() will be called
        # to allow a map with tiles to be produced.
        if colorbar_len == -1:
            colorbar_len = 0.8
        fig = px.choropleth_map(gdf, 
        geojson = gdf[geojson_col],
        locations = gdf.index,
        color = color,
        hover_data = [data_col] + extra_hover_cols, 
        color_continuous_scale = color_continuous_scale,
        title = title, 
        map_style=tile_source, zoom = zoom,
        center = {'lat':starting_loc[0], 'lon':starting_loc[1]},
        opacity=opacity)
        
    
    if margin_list is None:
        if show_tiles == True:
        # Setting each margin to 0 will allow the map to take up more
        # of the window--which can be particularly useful for tiled maps.
        # (This code is based on a snippet from
        # https://plotly.com/python/map-configuration/ .)
            fig.update_layout(margin = {
                    "r":0,"t":0,"l":0,"b":0})
        # No changes will be made in this case if show_tiles is set to
        # False.
        
    else: # Updating the margins (if requested by the user)
        fig.update_layout(margin = {
            "r":margin_list[0],"t":margin_list[1],
            "l":margin_list[2],"b":margin_list[3]})

    # This code will also shorten the colorbar a little so that
    # the reduced bottom margin does not cut off our title.
    # (This code was derived from
    # https://plotly.com/python/reference/layout/coloraxis/ )
    
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
            colorbar_tickvals = percentile_quantile_list,
            colorbar_tickmode = 'array',
            colorbar_ticktext = score_list,
            colorbar_title = colorbar_title,
            colorbar_title_side = 'bottom')

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
            gdf.at['Maryland', 'label_lat'] = 39.4
            gdf.at['Maryland', 'label_lon'] = -77.24
            
            gdf.at['Michigan', 'label_lat'] = 43.63
            gdf.at['Michigan', 'label_lon'] = -84.97
            
            gdf.at['Louisiana', 'label_lat'] = 30.5
            gdf.at['Louisiana', 'label_lon'] = -92.54
        

        # This code was based mostly on
        # https://plotly.com/python/scatter-plots-on-
        # maps/#simple-us-airports-map .
        fig.add_scattergeo(
            text = gdf[label_col],
            mode = 'text',
            lat = gdf['label_lat'],
            lon = gdf['label_lon'])

        # Disabling hover functionality for these text labels (as they
        # can interfere with the pre-existing labels):
        fig.update_traces(hoverinfo = 'skip', selector = dict(
            type='scattergeo'))
    # This code was based on
# https://plotly.com/python/reference/scattergeo/

    # Saving this map to HTML and static files 
    # (if requested by the caller):
    if (save_html == True) or (save_static == True):
        update_and_save_plotly_map(
            fig = fig, save_html = save_html, save_static = save_static, 
            static_file_folder = static_file_folder,
            html_file_folder = html_file_folder, filename = filename, 
            image_extension = image_extension, 
            include_plotlyjs = include_plotlyjs, 
            screenshot_label_font_size = screenshot_label_font_size,
            screenshot_width = screenshot_width, 
            screenshot_height = screenshot_height,
            screenshot_scale = screenshot_scale, 
            screenshot_title_y = screenshot_title_y,
            screenshot_title_font_size = screenshot_title_font_size, 
            screenshot_colorbar_thickness = screenshot_colorbar_thickness, 
            screenshot_colorbar_len = screenshot_colorbar_len, 
            screenshot_colorbar_tickfont_size = \
screenshot_colorbar_tickfont_size, 
            screenshot_colorbar_title_font_size = \
screenshot_colorbar_title_font_size)
        
    if debug == True:
        return fig, percentile_quantiles, score_list, gdf
    else:
        return fig