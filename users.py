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

warnings.filterwarnings("ignore")
conn = sqlite3.connect('data.sqlite')
engine = create_engine('sqlite:///data.sqlite')
db = SQLAlchemy()
config = configparser.ConfigParser()

c = conn.cursor()
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable = False)
    password = db.Column(db.String(80))
Users_tbl = Table('users', Users.metadata)

def create_users_table():
    Users.metadata.create_all(engine)

create_users_table() #WILL CREATE TABLE FROM FRESH EACH TIME APP STARTS

class Users(UserMixin, Users):
    ...