from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash
from app import app
from app import server
from layouts import layout_menu, layout_query_menu,layout_about
from layouts import layout_query_move 
from layouts import layout_register,login,failed,logout
from layouts import layout_front_page
from layouts import navbar_with_login
import callbacks
import users
import flask
import dash_auth
import pandas as pd
from flask import redirect, url_for

import sqlite3
from sqlalchemy import Table, create_engine
from sqlalchemy.sql import select
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, logout_user, current_user, LoginManager, UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

import warnings
import configparser
import os

server.config.update(
    SECRET_KEY=os.urandom(12),
    SQLALCHEMY_DATABASE_URI='sqlite:///data.sqlite',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)
users.db.init_app(server)

login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/'


# callback to reload the user object
@login_manager.user_loader
def load_user(user_id):
    return users.Users.query.get(int(user_id))

#MAIN APP LAYOUT - WHICH DISPLAYS NAVBAR
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar_with_login,
    html.Div(id='page-content'),
])
app.config.suppress_callback_exceptions = True


@login_manager.user_loader
def load_user(user_id):
    return users.Users.query.get(int(user_id))

#MAIN APP NAVIGATION SCHEME
@app.callback(
        Output('page-content', 'children'),
        Input('url', 'pathname')
             )
def display_page(pathname):
    if pathname == '/':
        return layout_front_page
    if pathname == '/login':
        return login
    elif pathname == '/register':
        return layout_register
    elif pathname == '/welcome':
        if current_user.is_authenticated:
            return layout_menu
        else:
            return failed
    elif pathname == '/about': return layout_about
    elif pathname == '/logout':
        if current_user.is_authenticated:
            logout_user()
            return logout
        else:
            return logout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True,port=5000) #,host='0.0.0.0'
