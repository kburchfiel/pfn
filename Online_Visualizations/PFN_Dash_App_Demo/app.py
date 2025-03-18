# Most of the following code derived from:
# https://community.plotly.com/t/dash-app-pages-
# with-flask-login-flow-using-flask/69507/37
# Note that Nader Elshehabi's code (on which this code was based)
# was released under the MIT license:
# https://github.com/naderelshehabi/dash-flask-login
# Ken Burchfiel incorporated some additional code from 
# https://dash.plotly.com/urls and https://dash-bootstrap-components.
# opensource.faculty.ai/docs/quickstart/ ;
# he also made minor edits to the display text.

"""
 CREDIT: This code was originally adapted for Pages based on Nader 
 Elshehabi's  
 article:
https://dev.to/naderelshehabi/securing-plotly-dash-using-flask-login-4ia2
https://github.com/naderelshehabi/dash-flask-login

This version was updated by Dash community member @jinnyzor . 
For more info, see:
https://community.plotly.com/t/dash-app-pages-with-
flask-login-flow-using-flask/69507

For other Authentication options, see:
Dash Enterprise: 
    https://dash.plotly.com/authentication#dash-enterprise-auth
Dash Basic Auth: 
    https://dash.plotly.com/authentication#basic-auth

"""


import os
from flask import Flask, request, redirect, session, jsonify, \
url_for, render_template
from flask_login import login_user, LoginManager, UserMixin, \
logout_user, current_user

import dash
from dash import dcc, html, Input, Output, State, ALL
import dash_bootstrap_components as dbc # See
# https://dash-bootstrap-components.opensource.faculty.ai/docs/quickstart/


# Exposing the Flask Server to enable configuring it for logging in
# Note that this code will be used in place of 
# server = app.server , which we used within our Simple_App_Without_Login
# app.
server = Flask(__name__)

@server.before_request
def check_login():
    if request.method == 'GET':
        if request.path in ['/login', '/logout']:
            return
        if current_user:
            if current_user.is_authenticated:
                return
            else:
                for pg in dash.page_registry:
                    if request.path == dash.page_registry[pg]['path']:
                        session['url'] = request.url
        return redirect(url_for('login'))
    else:
        if current_user:
            if request.path == '/login' or current_user.is_authenticated:
                return
        return jsonify(
            {'status':'401', 'statusText':'unauthorized access'})


@server.route('/login', methods=['POST', 'GET'])
def login(message=""):
    if request.method == 'POST':
        if request.form:
            username = request.form['username']
            password = request.form['password']
            if VALID_USERNAME_PASSWORD.get(username) is None:
                return """The username and/or password were \
invalid. <a href='/login'>Please try again.</a>"""
            if VALID_USERNAME_PASSWORD.get(username) == password:
                login_user(User(username))
                if 'url' in session:
                    if session['url']:
                        url = session['url']
                        session['url'] = None
                        return redirect(url) ## redirect to target url
                return redirect('/') ## redirect to home
            message = "The username and/or password were invalid."
    else:
        if current_user:
            if current_user.is_authenticated:
                return redirect('/')
    return render_template('login.html', message=message)

@server.route('/logout', methods=['GET'])
def logout():
    if current_user:
        if current_user.is_authenticated:
            logout_user()
    return render_template('login.html', 
                           message="You have now been logged out.")

app = dash.Dash(
    __name__, server=server, use_pages=True, 
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)
# See:
# https://dash-bootstrap-components.opensource.faculty.ai/docs/quickstart/

# Keep this out of source code repository - save in a file or a database
#  passwords should be encrypted
VALID_USERNAME_PASSWORD = {"test": "test", "hello": "world"}


# Updating the Flask Server configuration with Secret Key to encrypt 
# the user session cookie
# server.config.update(SECRET_KEY=os.getenv("SECRET_KEY"))
server.config.update(SECRET_KEY="insecureplaceholder")
# Definitely don't use the above approach in a real-world applicaiton!

# Login manager object will be used to login / logout users
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = "/login"


class User(UserMixin):
    # User data model. It has to have at least self.id as a minimum
    def __init__(self, username):
        self.id = username


@login_manager.user_loader
def load_user(username):
    """This function loads the user by user id. Typically this looks 
    up the user from a user database.
    We won't be registering or looking up users in this example, 
    since we'll just login using LDAP server.
    So we'll simply return a User object with the passed in username.
    """
    return User(username)

print(
    [(page['name'], page["relative_path"])
for page in dash.page_registry.values()])

# print(dash.page_registry.values())

app.layout = html.Div(
    [
        html.A('Log out', href='../logout'),
        html.Br(),

        # The following commented-out and active sections of the script
        # show three different ways of building a navigation menu.
        
        # html.H3("Page index:"), # Commented out--see notes below
        # The following html.Div() section came from:
        # https://dash.plotly.com/urls .
        # It places all pages on a separate line, which I found
        # to be unwieldy for apps like this one with larger page
        # counts.
    #     html.Div([
    #     html.Div(
    #         dcc.Link(f"{page['name']} - {page['path']}", 
    #                  href=page["relative_path"])
    #     ) for page in dash.page_registry.values()
    # ]),

        # This variant of the above commented-out code places all
        # pages on the same line (though, if the window isn't wide enough,
        # some pages may get placed on separate lines). It updates
        # automatically to incorporate page additions and deletions,
        # but it offers less control over page names and orders than the 
        # Markdown-based headers that follow it.
        # html.Div(
        #     [dcc.Link(f"{page['name']} | ", href=page["relative_path"])
        #     for page in dash.page_registry.values()]),

        # The following code shows a more manual, Markdown-based
        # approach to creating a navigation menu. Although the
        # Markdown will need to be updated manually to incorporate 
        # new pages, this approach allows both page names and orders
        # to be easily customized.
        # Note that the relative links shown within this example
        # suffice for navigation purposes; absolute links aren't 
        # necessary. (If they were, we might have needed to create 
        # separate links for offline and online deployments.)

        # For documentation on dcc.Markdown,
        # visit: https://dash.plotly.com/dash-core-components#markdown
        
        dcc.Markdown('''
### Page Index: 
[Home Page](/) |
[Fixed Dashboard](/fixed_dashboard) |
[Simple Interactive Dashboard](/simple_interactive_dashboard) 

[Flexible Survey Results Dashboard](/flexible_survey_results_dashboard) |
[Flexible Enrollment Dashboard](/flexible_enrollment_dashboard) |
[Dash Pivottable (Enrollment)](/dash_pivottable_enrollment) | 
[Dash Pivottable (Survey Results)](/dash_pivottable_survey_results)
'''),
        dash.page_container,

        # The following explanatory text will appear at the bottom of 
        # each page.
        dcc.Markdown('''        
*This site is part of [Python for Nonprofits]
(https://github.com/kburchfiel/pfn), created by Kenneth Burchfiel and 
licensed under the MIT License.*

*Blessed Carlo Acutis, pray for us!*
'''),
    ]
)


if __name__ == "__main__":
    app.run_server(debug=True)