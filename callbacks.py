from dash.dependencies import Input, Output, State
from app import app
import pandas as pd
import plotly.express as px
from layouts import layout_menu, layout_query_menu
from layouts import layout_query_move,login
import dash
from dash import html
from dash import dcc

from sqlalchemy import Table, create_engine
from sqlalchemy.sql import select
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import warnings
import os
from flask_login import login_user, logout_user, current_user, LoginManager, UserMixin
import configparser

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, LoginManager, UserMixin

from pathlib import Path
import time
import datetime
from datetime import timedelta
import sys

import users

app.validation_layout = html.Div([layout_query_move,])

def visualise_output(df):
    return px.scatter(df, x=[0,0], y=[0,0])

#CALLBACK FOR SHOWING CONDITIONAL INPUT BOXES
@app.callback(
    Output('graph0', 'figure'),
    Input('submit-button-state-go-run-query', 'n_clicks'),
    State('EVENT_ID_state', 'value'), #
    State('MASTER_TICKER_STR_state', 'value'),
    State("full-input-boxes", "children"),
             )
def display_value0(n_clicks,event_id,master_ticker_str, children):
    df = pd.DataFrame(data={'x': [0, 0], 'y': [0, 0]})
    fig = px.scatter(df, x=[0,0], y=[0,0])
    fig_pg_0 = fig
    if children: 
        fig_pg_0 = visualise_output(df)
        #if children == type0 --> process input method 0
        #if children == type1 --> process input method 1
    return fig_pg_0

@app.callback(
    Output('full-input-boxes', 'children'),
    Input('submit-button-choose-event', 'n_clicks'),
    State('EVENT_ID_state', 'value'),
)
def ask_for_more_inputs(n_clicks,event_id):
    if not n_clicks: raise dash.exceptions.PreventUpdate
    if event_id == 'MOVE': return layout_query_move
    return layout_query_fundamental

#LOGIN FORMS
@app.callback(
    Output('url_logout', 'pathname'),
    [Input('back-button', 'n_clicks')])
def logout_dashboard(n_clicks):
    if n_clicks > 0: return '/register'

@app.callback(
    [Output('container-button-basic', "children"),
     #Output('url_loginxx', 'pathname')
     ],
    [Input('submit-val', 'n_clicks')],
    [
        State('email_username', 'value'),
        State('password', 'value'),
    ]
)
def insert_users(n_clicks, email_username, pw):
    hashed_password = ''
    if pw is not None: hashed_password = generate_password_hash(pw, method='sha256')
    if email_username is not None and pw is not None: #is not None:
        ins = users.Users_tbl.insert().values(username=email_username, password=hashed_password)
        conn = users.engine.connect()
        conn.execute(ins)
        conn.close()
        return [html.Div([html.H2('registration successful!'),login])] #redirect(url_for('/'))
    else:
        if email_username is not None:
            if '@' not in email_username:
                return [html.Div([html.H2('error: invalid username')])]
        if pw is not None:
            if len(pw) <6:
                return [html.Div([html.H2('error: password too short')])]
        errors = False
        if errors == False: return [html.Div([html.H2('')])]

@app.callback(
    Output('url_login', 'pathname')
    , [Input('login-button', 'n_clicks')]
    , [State('uname-box', 'value'), State('pwd-box', 'value')])
def successful(n_clicks, input1, input2):
    user = users.Users.query.filter_by(username=input1).first()
    if user:
        if check_password_hash(user.password, input2):
            login_user(user)
            return '/welcome'
        else:
            pass
    else:
        pass

@app.callback(
    Output('output-state', 'children')
    , [Input('login-button', 'n_clicks')]
    , [State('uname-box', 'value'), State('pwd-box', 'value')])
def update_output(n_clicks, input1, input2):
    if n_clicks > 0:
        user = users.Users.query.filter_by(username=input1).first()
        if user:
            if check_password_hash(user.password, input2):
                return ''
            else:
                return 'Incorrect username or password'
        else:
            return 'Incorrect username or password'
    else:
        return ''

@app.callback(
    Output('url_login_success', 'pathname')
    , [Input('back-button', 'n_clicks')])
def logout_dashboard(n_clicks):
    if n_clicks > 0: return '/register'

@app.callback(
    Output('url_login_df', 'pathname')
    , [Input('back-button', 'n_clicks')])
def logout_dashboard(n_clicks):
    if n_clicks > 0: return '/register'