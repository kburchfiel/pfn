# Helper functions that will prove useful for multiple sections of
# Python for Nonprofits

# By Kenneth Burchfiel

# Released under the MIT license

from IPython.display import Image # Based on 
# a StackOverflow answer from 'zach' at
# https://stackoverflow.com/a/11855133/13097194 .
import pandas as pd

render_for_pdf = True # Setting this variable here, and passing it to the
# config_notebook() function defined below by default, makes it easier 
# to update the output of multiple notebooks (i.e. when running
# jupyter-book code to produce either PDF or HTML versions of 
# Python for Nonprofits).

def config_notebook(render_for_pdf=render_for_pdf, 
                    display_max_columns = 6,
                   display_max_rows = 5,
                   debug = False):
    '''
    This function helps modify several settings in order to prepare
    a Jupyter notebook for either print or HTML display.
    
    render_for_pdf: set to True to optimize notebook outputs for PDF
    display. (This setting can also improve the appearance of notebooks
    on GitHub.) Set to False to optimize notebooks outputs for interactive
    viewing. Note that, unless this value is specified by the caller,
    the render_for_pdf value within helper_funcs.py will be passed
    to this function.
    
    display_max_columns and display_max_rows: the maximum number of 
    DataFrame columns and rows, respectively, to display when
    render_for_pdf is set to True. Limiting these values can prevent 
    DataFrames from taking up too much space within PDF copies of 
    notebooks.

    debug: set to True in order to print out additional information
    about the values set by this function.
    '''
    
    if render_for_pdf == True:
        pd.set_option('display.max_columns', display_max_columns)
        pd.set_option('display.max_rows', display_max_rows)
        display_type = 'png' # Will instruct a chart display function
        # to return .png versions of charts (which may show up better
        # within PDF versions of this script than would HTML copies)
    else:
        display_type = 'html' # In this case, HTML versions of the charts
        # will be featured instead.
    if debug == True:
        print(f"render_for_pdf: {render_for_pdf}\nmax df columns: \
{display_max_columns}\nmax df rows: {display_max_rows}\ndisplay_type: \
{display_type}")
    return display_type # Returning this variable allows it to get
    # passed to wadi().
    
    
        

def wadi(fig, file_path, height=405, aspect_ratio=16/9,
         width=None, scale=None, include_plotlyjs='cdn',
         display_type='html', display_width=720, html_path_prefix='',
         static_path_prefix='', debug=False, 
         generate_image=True, display_image = True):
    '''This function saves the Plotly figure passed to 'fig' to the 
    destination represented by 'file_path', then displays it as either
    an .html or .png file depending on the value of display_type. It can
    also display graphics that weren't created within Plotly (such as
    Folium maps).
    
    'height', 'width', and 'scale' will get passed to the parameters of 
    the same name within a px.write_image() call. Don't add .png or 
    .html to the end of file_path; these will get added in automatically 
    by the function.

    By default, the image width will get initialized as the product
    of the image's height and aspect ratio. This makes it easier to 
    increase or decrease image sizes without having to manually 
    recalculate the width each time. 

    Similarly, if the scale parameter is not manually set by the 
    caller, it will get initialized as 2160 divided by the height. 
    This will produce an image with a height of 2160 pixels by 
    default (as (2160 / height) * height = 2160).

    include_plotlyjs: The argument to pass to the respective 
    include_plotlyjs parameter within write_html(). The default setting
    allows for smaller HTML file sizes; however, if it's important for
    your maps to render offline, select True as your argument instead.
    For more details on these and other options, consult 
    https://plotly.com/python-api-reference/generated/
    plotly.io.write_html.html .
    
    display_type: set to .png to use IPython's Image() function to 
    return the static image created within the function. (The width of 
    this image will equal display_width.) If set to 'html', on the other
    hand, an HTML rendition of the figure will be returned. 
    (If a different Plotly default image renderer was specified within
    the notebook, the image will be displayed using that format instead.)

    display_width: The width, in pixels, to display a screenshot. This 
    setting will only get applied if display_type is set to 'png.' 

    If you would like to store .html and .png images within different
    folders, pass those folder names to html_path_prefix and
    static_path_prefix, respectively. These names will then get added
    to the beginning of copies of file_path. If you keep these values
    as empty strings, file_path will get used as the save destination
    for both HTML and PNG files.

    debug: Set to True to print various details about the .png image
    that this function creates.

    generate_image: set to False in order to skip the process of
    creating HTML and PNG files for the figure (e.g. because they have
    already been rendered).

    display_image: set to False if you do not wish to display your image
    after creating it.
    
    ('wadi' stands for 'write and display image.')
    '''

    # Setting the folder paths for both the .html and .png copies
    # of each file:
    static_file_path = static_path_prefix + file_path
    html_file_path = html_path_prefix + file_path
    if width == None:
        width = height * aspect_ratio 

    if scale == None:
        scale = 2160 / height

    if debug == True:
        print(f"Height: {height}, width: {width}, aspect ratio: \
{aspect_ratio}, scale: {scale}, HTML file path: {html_file_path}.html, \
static file path: {static_file_path}.png, display type: {display_type}, \
generate_image: {generate_image}")

    if generate_image == True:
        # Saving .html and .png copies of the file:
        fig.write_html(html_file_path+'.html', 
                       include_plotlyjs=include_plotlyjs)
        fig.write_image(static_file_path+'.png', height=height, 
                        width=width, scale=scale)
    if display_image == True:
        if display_type == 'png':
            return Image(static_file_path+'.png', width=display_width)
            # Source: StackOverflow user 'zach' at
            # https://stackoverflow.com/a/11855133/13097194
        else:
            return fig # The function could instead load and display the
            # .html image stored at html_file_path, but this approach is 
            # simpler and should still work fine in most cases.