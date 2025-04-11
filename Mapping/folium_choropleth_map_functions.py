# Folium-based choropleth map functions

import folium
import geopandas
import numpy as np
import time
import os
from branca.utilities import color_brewer
# color_brewer source code: 
# https://github.com/python-visualization/branca/blob/main/branca/
# utilities.py

from selenium import webdriver

import branca.colormap as cm
# From https://python-visualization.github.io/folium/latest/
# advanced_guide/colormaps.html#StepColormap
from branca.colormap import StepColormap # From Folium's features.py
# source code: 
# https://github.com/python-visualization/folium/blob/main/
# folium/features.py




def cptt(
    starting_lat, starting_lon, gdf, 
    data_col, boundary_name_col,
    data_col_alias, boundary_name_alias,
    zoom_start=6, 
    bin_type='linear', 
    bin_count=6, custom_threshold_list=[], 
    color_scheme='RdYlBu',
    tooltip_variable_list=[], tooltip_alias_list=[],
    save_html=True, save_screenshot=True,
    driver_window_width=3000,
    driver_window_height=1688,
    map_filename='map', html_map_folder='',
    png_map_folder='',
    geometry_col='geometry',
    tiles='OpenStreetMap', choropleth_opacity=0.6,
    add_boundary_labels=False, boundary_label_lon_shift=10,
    boundary_label_lat_shift=10, boundary_label_col='',
    round_boundary_labels=False,
    boundary_label_round_val=0,
    delete_html_file=False): 
    
    '''This function creates a chorolpeth map with a set of tooltips
    via folium.GeoJson(). (cptt stands for 'chorolpeth and tooltip.' 
    Creating these two items together saves
    storage space versus building them individually.
    The function also adds in boundary labels upon request.

    Note: Much of this function is based on the sample code found at 
    https://python-visualization.github.io/folium/latest/user_guide/
    geojson/geojson_popup_and_tooltip.html
    and https://python-visualization.github.io/folium/latest/user_guide/
    geojson/geojson.html .
    
    starting_lat, starting_lon, and zoom_start: the initial latitude,
    longitude, and zoom to pass to folium.Map(), respectively. For maps
    of the contiguous 48 US states, consider using a starting latitude 
    of 38 and a starting longitude of -95.
    
    gdf: A GeoDataFrame containing both boundary outlines and statistical
    data to visualize. Note that, in order to reduce the size of the 
    resulting map, gdf will be condensed to include only those columns 
    necessary for creating the map and adding in tooltips.
    
    data_col: the column within gdf containing data to visualize.
    
    boundary_name_col: the column within gdf that displays names of
    the boundaries being visualized.

    data_col_alias and boundary_name_alias: The labels to use for
    data_col and county_boundary_name_col, respectively, within the 
    map's tooltips.
        
    tooltip_variable_list: A list of variables 
    (other than boundary_name_col
    and data_col, which will get added in automatically) 
    to display within the tooltip.

    bin_type: Set to 'linear' (the default argument) to create 
    equally spaced bins; 'percentile' to base choropleth colors on 
    percentiles (resulting in roughly equal numbers of results per bin);
    or 'custom' to pass in a list of custom bins. (The custom option can 
    be particularly useful when you wish to use the same set of bins for 
    multiple maps.)

    bin_count: The number of separate colors to show within the map. This
    parameter will be ignored when bin_type is set to 'custom.'

    custom_threshold_list: A list of custom bin ranges to use for the map.
    Will only get applied when bin_type is set to 'custom.'
        
    color_scheme: The color scheme to use within the map (e.g. 'RdYlBu'). 
    Options can be found on https://colorbrewer2.org/ . 
    In order to reverse
    a scheme, add '_r' to the end (e.g. 'RdYlBu_r'). Source:
    https://github.com/python-visualization/branca/blob/main/branca/
    utilities.py

    save_html: set to True to save this map as an HTML file.
    
    save_screenshot: set to True in order to generate a screenshot of 
    the map, then save it as a .PNG file. In order for this screenshot 
    to get created, save_html must also be set to True.

    driver_window_width and driver_window_height: the default width and 
    height, respectively, of the Selenium driver window that will be 
    called to generate a screenshot. The default settings work well 
    for maps of the contiguous United States.

    map_filename: The name to use when saving the map. The script will add
    the correct extension (e.g. 'html') to this map, so leave that portion
    out of the argument.

    html_map_folder and png_map_folder: The folders 
    in which to store HTML and PNG versions of maps, respectively. 
    Note that, if you're generating screenshots, html_map_folder needs 
    to be an absolute path (so that it can get interpreted correctly by 
    the Selenium-driven browser). For instance, if your html_map_folder 
    is titled 'maps' and stored within your directory, pass 
    os.getcwd()+'/maps' as your html_map_folder argument.

    geometry_col: The column in gdf that stores shape boundary data.

    Tiles: the tile provider to use for your map. Note that different tile 
    services use different licenses for their tiles. If you don't want 
    to use any tiles, enter None (no quotes) as your argument 
    for this parameter.

    choropleth_opacity: a float, ranging from 0 to 1, that determines
    how opaque to make the colors within the choropleth map. If tiles 
    is set to None, consider setting choropleth_opacity to 1.

    add_boundary_labels: Set to True to label each boundary within 
    the map.
    
    boundary_label_lon_shift and boundary_label_lat_shift: Integers that 
    specify how far west and north to shift boundary labels so that they 
    appear more centered. (These values will get passed to the 
    icon_anchor parameter of the DivIcons.)

    boundary_label_col: The column to use as a source for boundary labels.
    You may choose to set this to be the same as data_col or boundary_name
    col, but you're not limited to those options.

    round_boundary_labels: set to True to round boundary labels by
    boundary_label_round_val (see below).

    boundary_label_round_val: An integer specifying the amount by which to 
    round the boundary labels. Set to 0 to round to whole numbers, to 1 to
    round to tenths, and so forth.

    delete_html_file: set to True in order to delete the HTML file saved 
    by this function. (This can be useful when you are only calling this 
    function only to create a screenshot of a map. Once the screenshot 
    has been saved, the original HTML file no longer needs to be 
    retained.) Note that, if save_html is set to False, the program 
    will *not* attempt to delete the HTML file, as it's likely that one 
    doesn't exist to begin with.
    '''

    
    # You can uncomment the following two print statements to compare
    # the sizes of gdf and gdf_condensed.
    
    # print(gdf.memory_usage(deep=True).sum() / 1000000)
    # See https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.
    # memory_usage.html

    # Creating a condensed version of gdf that can serve as the basis for 
    # the map: (Condensing the DataFrame prevents unnecessary columns
    # from getting included in the HTML output and thus increasing
    # the map's file size.)

    gdf_condensed = gdf.copy()[
    [boundary_name_col, data_col, geometry_col] + tooltip_variable_list]

    # Removing any NaN data_col entries from our dataset so that they
    # won't interfere with our mapping code:
    # {data_col} is surrounded by ` characters to make this code 
    # compatible with column names that contain spaces.
    gdf_condensed.query(f"`{data_col}`.isna() == False", inplace=True)

    # print(gdf_condensed.memory_usage(deep=True).sum() / 1000000)

    # Creating a blank map as the starting point for our choropleth:
    m = folium.Map([starting_lat, starting_lon], 
                   zoom_start=zoom_start, tiles=tiles,
                  zoom_control=False)

   
    # Adding labels to each boundary:
    # (Note: this code will work better for larger shapes, such as US 
    # states, and likely less well for smaller boundaries like counties 
    # or zip codes.)
    # Adding these labels prior to creating our tooltips ensures that
    # the former won't block the latter when the user is interacting with
    # the map.

    # Calculating reference points for adding labels to each boundary:
    # The following code applies GeoPandas' representative_point() method
    # to calculate central points for each boundary that always lie within
    # that boundary. It then uses a list comprehension to create lists of
    # x and y coordinates that can be fed into folium mapping code.
    # (The POINT items returned by representative_point() don't appear
    # to work as well with Folium.)

    if add_boundary_labels == True:
        gdf_condensed['boundary_label_reference_points'] = [
            [coord.y, coord.x] for coord in 
         gdf_condensed['geometry'].representative_point()]
        # Documentation for representative_point(): 
        # https://geopandas.org/en/stable/docs/reference/api/geopandas.
        # GeoSeries.representative_point.html#geopandas.GeoSeries.
        # representative_point
        # x and y are attributes of Geoseries objects:
        # https://geopandas.org/en/stable/docs/reference/geoseries.html
    
    
        # Using these reference points to add the values stored
        # in boundary_label_col as boundary labels:
        for i in range(len(gdf_condensed)):
            boundary_label = gdf_condensed.iloc[i][
            boundary_label_col].copy()
            if round_boundary_labels == True:
                boundary_label = boundary_label.round(
                    boundary_label_round_val)
            folium.Marker(location=gdf_condensed.iloc[i][
                          'boundary_label_reference_points'],
                         icon=folium.features.DivIcon(
                             f"<b>{boundary_label}</b>",
                         icon_anchor=(boundary_label_lon_shift, 
                                        boundary_label_lat_shift))
                         ).add_to(m)
        # Part of the folium.Marker() call above is based on an example 
        # by StackOverflow user 'r-beginners'
        # (who pointed out that you could pass a DivIcon to the 'icon' 
        # parameter 
        # within a Marker in order to add text labels to shapes). 
        # Source: https://stackoverflow.com/a/72588910/13097194
        # The use of icon_anchor to adjust the labels' locations
        # comes from the DivIcon documentation at:
        # https://python-visualization.github.io/folium/latest/
        # reference.html#folium.features.DivIcon
    
    
    # Creating the tooltips:

    tooltip_field_list = [
        boundary_name_col, data_col] + tooltip_variable_list

    alias_list = [boundary_name_alias, 
                  data_col_alias] + tooltip_alias_list

    
    # print(tooltip_field_list, alias_list)
    
    tooltip = folium.GeoJsonTooltip(
        fields= tooltip_field_list,
        aliases=alias_list,
        localize=True,
        sticky=False,
        labels=True,
        style="""
            background-color: #FFFFFF;
            border: 1px;
            border-radius: 1px;
            box-shadow: 1px;
        """,
        max_width=800
    )
    
    # Creating our set of colors to use for the choropleth map:
    if bin_type == 'custom': # In this case, bin_count will be overwritten
        # by the length of custom_threshold_list minus 1. (The number of
        # bins will always be one less than the number of thresholds, as 
        # two thresholds are needed to establish the boundaries for 
        # one bin.
        # For instance, if you have three thresholds (0, 1, and 2),
        # two bins can be created from this list: 0-1 and 1-2.)
        bin_count = len(custom_threshold_list) - 1
    color_range = color_brewer(color_scheme, n=bin_count)
    # Based on Choropleth() definition within
    # https://github.com/python-visualization/folium/blob/main/folium/
    # features.py
    
    # To reverse the set of colors passed to color_scheme, add '_r' 
    # to the end of the string (e.g. 'RdYlBu_r'). Source: 
    # https://github.com/python-visualization/branca/blob/main/branca
    # /utilities.py


    # Determining which colors to apply to each result:
    
    if bin_type == 'linear': # Equally-spaced bins will be used. 
        # The number of bins will be derived from the number of 
        # colors in color_range.
        stepped_cm = StepColormap(
            colors=color_range, 
            vmin=gdf_condensed[data_col].min(),
            vmax=gdf_condensed[data_col].max())
        # Based on: 
        # https://python-visualization.github.io/branca/colormap.html#
        # branca.colormap.StepColormap

    else: # In this case, a different approach to creating the 
        # StepColorMap
        # will be used that better accommodates non-equally-spaced bins.
        
        if bin_type == 'percentile': # In this case, 
            # percentile-based bins will
            # be used.
            bin_thresholds = list(gdf_condensed[data_col].quantile(
            np.linspace(0, 1, bin_count+1))) 
            # For np.linspace() documentation, see:
            # https://numpy.org/doc/stable/reference/generated/
            # numpy.linspace.html
    
        elif bin_type == 'custom': # This condition allows for a set of 
            # custom bins to be passed in.
            bin_thresholds = custom_threshold_list.copy()

        else:
            raise ValueError("bin_type must be set to 'linear', \
'percentile, or 'custom.'")
        
        # The following approach works for both 'percentile' and 
        # 'custom' bin_type conditions.
        stepped_cm = StepColormap(
            colors=color_range, 
            vmin=bin_thresholds[0], vmax=bin_thresholds[-1],
            index=bin_thresholds)
        # Based on the self.color_scale initialization within Folium's 
        # Choropleth()  source code (available at
        # https://github.com/python-visualization/folium/blob/main/
        # folium/features.py )

    
    # The following code will both assign colors from StepColorMap
    # to each region *and* add in tooltips. This approach allows the
    # colors and tooltips to reference the same set of outlines,
    # thus allowing for a smaller file size.
    
    g = folium.GeoJson(
        gdf_condensed,
        style_function=lambda x: {
            "fillColor": stepped_cm(
                x["properties"][data_col]),
            "fillOpacity": choropleth_opacity,
            "weight":1,
            "color":"black"
        },
        tooltip=tooltip
    ).add_to(m)
    # The Folium.GeoJSON overview at
    # https://python-visualization.github.io/folium/latest/
    # user_guide/geojson/geojson.html
    # contributed to this code as well.
    # Note that we need to add ["properties"] in between x and 
    # [data_col], likely because gdf_condensed
    # is being interpreted as a GeoJSON object. I based this off of the
    # "if "e" in feature["properties"]["name"].lower()" line within
    # the above link.

    # Adding the color legend for the choropleth to the map:
    stepped_cm.add_to(m)
    # Based on:
    # https://python-visualization.github.io/folium/latest/user_guide/
    # geojson/geojson.html

    if save_html == True:
        m.save(f"{html_map_folder}/{map_filename}.html")

    # Generating a screenshot of the map:
    if save_screenshot == True:
        print("Generating screenshot.")
        options = webdriver.ChromeOptions()
        # Source: https://www.selenium.dev/documentation/webdriver/
        # browsers/chrome/
        options.add_argument(f'--window-size={driver_window_width},\
{driver_window_height}') # I found that this window
        # size, along with a starting zoom of 6 within our mapping code,
        # created a relatively detailed map of the contiguous 48 US 
        # states. 
        # If you'd like to create an even more detailed map, 
        # consider setting your starting zoom to 7 and your window size 
        # to 6000,3375.
        options.add_argument('--headless') # In my experience, this 
        # addition  (which prevents the Selenium-driven browser from 
        # displaying on your computer) was necessary for allowing 4K 
        # screenshots to get saved
        # as 3840x2160-pixel images. Without this line, the 
        # screenshots would  get rendered with a resolution of 
        # 3814x1868 pixels.
        # Source of the above two lines:  
        # https://www.selenium.dev/documentation/webdriver/
        # browsers/chrome/
        # and
        # https://github.com/GoogleChrome/chrome-launcher/blob/
        # main/docs/chrome-flags-for-tools.md
        # I learned about the necessity of using headless mode 
        # *somewhere* on  StackOverflow. Many answers to the question
        # linked below regarding generating screenshots reference it 
        # as an important step, for instance.
        # https://stackoverflow.com/questions/41721734/take-screenshot
        # -of-full-page-with-selenium-python-with-chromedriver/57338909

        
        # Launching the Selenium driver:
        driver = webdriver.Chrome(options=options) 
        # Source: https://www.selenium.dev/documentation/webdriver/
        # browsers/chrome/
        
        # Navigating to our map:
        # Note: In order to get the following code to work within
        # Linux, I needed to precede the local path with 'file://' as 
        # noted by GitHub user lukeis here: 
        # https://github.com/seleniumhq/selenium-google-code-issue-
        # archive/issues/3997#issuecomment-192014472
        driver.get(f"file://{html_map_folder}/{map_filename}.html")
        # Source: https://www.selenium.dev/documentation/
        time.sleep(3) # Helps ensure that the browser has enough 
        # time to download
        # map contents from the tile provider. This time might need to be
        # increased if a slow internet connection is in use. Conversely,
        # if no tiles are being incorporated into the map, 
        # there may not be any need to call
        # time.sleep().
        # Taking our screenshot and then saving it as a PNG image:
        driver.get_screenshot_as_file(
            f"{png_map_folder}/{map_filename}.png")
        # Source: 
        # https://selenium-python.readthedocs.io/api.html#selenium.
        # webdriver.remote.webdriver.WebDriver.get_screenshot_as_file
        
        # Exiting out of the webdriver:
        driver.quit()
        # Source: https://www.selenium.dev/documentation/
    
    if (delete_html_file == True) & (save_html == True):
        os.remove(f"{html_map_folder}/{map_filename}.html")
        print("Removed HTML copy of map.")
    
    return m


def create_map_and_screenshot(
    starting_lat, starting_lon, gdf, 
    data_col, boundary_name_col,
    data_col_alias, boundary_name_alias,
    html_zoom_start=5,
    screenshot_zoom_start=6, 
    bin_type='linear', bin_count=6, 
    custom_threshold_list=[],
    color_scheme='RdYlBu',
    tooltip_variable_list=[], tooltip_alias_list=[],
    map_filename='map', html_map_folder='',
    png_map_folder='',
    geometry_col='geometry',
    tiles='OpenStreetMap', choropleth_opacity=0.6,
    add_boundary_labels=False, boundary_label_lon_shift=10,
    boundary_label_lat_shift=10, boundary_label_col='',
    round_boundary_labels=False,
    boundary_label_round_val=0): 
    '''This function calls cptt() twice in order to create separate PNG
    and HTML versions of a map. This approach allows separate zoom levels
    to be passed to each map, which can prevent one or both maps from 
    displaying a non-ideal zoom level.
    
    html_zoom_start and screenshot_zoom_start: the zoom settings to use
    for the HTML and PNG maps, respectively.
    
    For information on other variables, consult the documentation within 
    cptt().'''

    # Creating an HTML map optimized for generating a screenshot;
    # creating the screenshot; and then deleting the HTML copy of the map
    # (as we only needed it in order to create the screenshot):
    cptt(
    starting_lat=starting_lat, 
        starting_lon = starting_lon, gdf=gdf, 
    data_col=data_col, boundary_name_col=boundary_name_col,
    data_col_alias=data_col_alias, 
        boundary_name_alias=boundary_name_alias,
    zoom_start=screenshot_zoom_start, 
    bin_type=bin_type, 
    bin_count=bin_count, 
    custom_threshold_list=custom_threshold_list, 
    color_scheme=color_scheme,
    tooltip_variable_list=tooltip_variable_list, 
        tooltip_alias_list=tooltip_alias_list,
    save_html=True, save_screenshot=True,
    map_filename=map_filename, html_map_folder=html_map_folder,
    png_map_folder=png_map_folder,
    geometry_col=geometry_col,
    tiles=tiles, choropleth_opacity=choropleth_opacity,
    add_boundary_labels=add_boundary_labels, 
        boundary_label_lon_shift=boundary_label_lon_shift,
    boundary_label_lat_shift=boundary_label_lat_shift, 
        boundary_label_col=boundary_label_col,
    round_boundary_labels=round_boundary_labels,
    boundary_label_round_val=boundary_label_round_val,
    delete_html_file=True)

    
    # Creating a copy of the map optimized for interactive viewing:
    # (This HTML file will get retained, whereas that created in order to 
    # produce the screenshot in the earlier cptt() call got deleted.)
    # Note that this code was called *after* the screenshot generation
    # code so that the latter's HTML map doesn't overwrite this one.
    m = cptt(
    starting_lat=starting_lat, 
        starting_lon=starting_lon,gdf=gdf, 
    data_col=data_col, boundary_name_col=boundary_name_col,
    data_col_alias=data_col_alias, 
        boundary_name_alias=boundary_name_alias,
    zoom_start=html_zoom_start, 
    bin_type=bin_type, 
    bin_count=bin_count, 
    custom_threshold_list=custom_threshold_list, 
    color_scheme=color_scheme,
    tooltip_variable_list=tooltip_variable_list, 
        tooltip_alias_list=tooltip_alias_list,
    save_html=True, save_screenshot=False,
    map_filename=map_filename, html_map_folder=html_map_folder,
    png_map_folder=png_map_folder,
    geometry_col=geometry_col,
    tiles=tiles, choropleth_opacity=choropleth_opacity,
    add_boundary_labels=add_boundary_labels, 
        boundary_label_lon_shift=boundary_label_lon_shift,
    boundary_label_lat_shift=boundary_label_lat_shift, 
        boundary_label_col=boundary_label_col,
    round_boundary_labels=round_boundary_labels,
    boundary_label_round_val=boundary_label_round_val,
    delete_html_file=False) 

    # Returning the map:
    return m

