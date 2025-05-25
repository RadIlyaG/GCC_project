# drilldown_app.py
import dash
from dash import dcc, html, dash_table, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
from datetime import date, timedelta, datetime
import os
import signal
import plotly.graph_objects as go
from collections import defaultdict
import time
import threading
import requests
import tkinter as tk
from tkinter import messagebox
import flask

from GetData import Qsfc, DrawPlot
from sql_db_rw import SqliteDB

shutdown_flag = {"exit": False}

def create_app(data):
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    #app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.title = "QSFC Data Vizualisation"



    app.layout = html.Div([
        #dcc.Graph(figure=fig),
        dbc.Row([
            dbc.Col(
                #html.H1("QSFC Data"),
            ),
            dbc.Col(
                #html.H4("by Dash system")
            ),
        ]),
        dbc.Row([
            dbc.Col(
                html.Div("Pick the dates"),
                width=2,
            ),
            dbc.Col(
                dbc.Button("apply dates", id='apply_dates', n_clicks=0,
                           className='mr-2'),
                width=1,
            ),
            dbc.Col(
                html.Div([
                    html.Div("FROM date"),
                    dcc.DatePickerSingle(
                        id='date-picker-from',
                        #date=(date.today() - timedelta(days=365)).strftime("%d/%b/%Y"),
                        display_format='YYYY-MM-DD',
                        #date=date.today() - timedelta(days=365),
                        #date=date.today() - timedelta(days=60),
                        date='2025-01-01'
                    ),
                ]),
                width=1,
            ),
            dbc.Col(
                html.Div([
                    html.Div("UPTO date"),
                    dcc.DatePickerSingle(
                        id='date-picker-upto',
                        date=date.today(),
                        #date=date.today().strftime("%d/%m/%Y"),
                        display_format='YYYY-MM-DD'
                    ),
                    #html.Div(id='output-container-date-picker-single')
                ]),
                width=1,
                ),
            dbc.Col(
                html.Div([
                    html.Div(id='output-container-date-picker-single')
                ]),
                width=0,
            ),
            dbc.Col(
                html.Div([
                    dcc.Dropdown(
                        id='dd_all_when',
                        options=[
                            {'label': 'Per Category', 'value': 'all'},
                            {'label': 'Per Date', 'value': 'when'},
                        ],
                        value='all',  # default value
                        clearable=False,  # can't clear the entry
                        multi=False
                    ),
                    html.Div(id='ddcategories')
                ]),
                width=2,
            ),
            dbc.Col(
                html.Div([
                    dcc.Dropdown(
                        id='dropdown-categories',
                        options=[
                            {'label': 'Product Line', 'value': 'product_line'},
                            {'label': 'Catalog', 'value': 'catalog'},
                            {'label': 'CSL', 'value': 'csl'}
                        ],
                        value='product_line',  # default value
                        clearable=False,  # can't clear the entry
                        multi=False
                    ),
                    html.Div(id='categories')
                ]),
                width=2,
            ),
        ], class_name='row_style',
        ),
        dbc.Row([
            dbc.Col(
                dbc.Button('Draw Graph', id='get_data', n_clicks=0,
                           className='mr-2'),
                width=1,
            ),
            dbc.Col(
                #html.Div(dcc.Graph(figure=fig), id='plot_place'),
                dcc.Graph(id='main-chart',
                          style={"height": "80vh"}
                          ),
                width=11,

            ),
            #dbc.Col(
            #    html.Div("spare place")
            #),
        ]),

        
    ])
    
    register_callbacks(app)

    return app
    
def register_callbacks(app):
    @app.callback(
        Output('output-container-date-picker-single', 'children'),
        [Input('apply_dates', 'n_clicks')],
        [State('date-picker-from', 'date'),
        State('date-picker-upto', 'date')])
    def update_output(n, start_date, end_date):
        print('apply_dates','n:', n, start_date, end_date)
        string_prefix = 'You have selected: '
        if start_date is not None:
            try:
                start_date_object = date.fromisoformat(start_date)
            except ValueError:
                string_prefix = string_prefix + 'Start Date: ' + start_date + ' | '
            else:
                start_date_string = start_date_object.strftime('%d/%m/%Y')
                string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
            #string_prefix = string_prefix + 'Start Date: ' + start_date + ' | '
            #print(f'1, {string_prefix}')
        if end_date is not None:
            try:
                end_date_object = date.fromisoformat(end_date)
            except ValueError:
                string_prefix = string_prefix + 'End Date: ' + end_date
            else:
                end_date_string = end_date_object.strftime('%d/%m/%Y')
                string_prefix = string_prefix + 'End Date: ' + end_date_string
            #string_prefix = string_prefix + 'End Date: ' + end_date
            #print(f'2, {string_prefix}')
        if len(string_prefix) == len('You have selected: '):
            return 'Select a date to see it displayed here'
        else:
            #print(f'3, {string_prefix}')
            return ''  #string_prefix

    @app.callback(
        [Output('main-chart', 'figure')],
        [Input('main-chart', 'clickData'),
         Input('get_data', 'n_clicks'),
         Input('dropdown-categories', 'value'),
         Input('dd_all_when', 'value')],
        [State('date-picker-from', 'date'),
         State('date-picker-upto', 'date')]
        )
    def update_chart(clickData, n, ret_cat, all_when, date_from, date_upto):
        if not n:
            return [go.Figure()]  # пустой график до нажатия

        print('update_chart','n:', n, 'date_from:', date_from,  'date_upto:', date_upto,
              'ret_cat:', ret_cat, 'all_when:', all_when)

        from dash import callback_context
        print("Triggered by:", callback_context.triggered)
        print("clickData:", clickData)

        sql = SqliteDB()
        dp = DrawPlot()
        options = {
            'cat': 'failure_desc',
            'tit': 'Failure Types of ETX-203AX',
            'xaxis_tit': 'Failure Types',
            'yaxis_tit': 'Quantity',
            'chart_type': 'bar',
        }
        #df = sql.read_table('RMA', date_from, date_upto, ret_cat=['failure_desc'], cat='product_line', cat_val="ETX-203AX")
        #fig = dp.by_category(df, **options)
        options = {
            'cat': ret_cat,
            'tit': 'Total RMAs',
            'xaxis_tit': 'RMAs',
            'yaxis_tit': 'Quantity',
            'chart_type': 'bar',
            'drill_plot_only' : True,
        }
        df = sql.read_table('RMA', date_from, date_upto, ret_cat=[ret_cat])
        if all_when=='when':
            fig = dp.by_cat_day(df, **options)
        elif all_when=='all':
            fig = dp.by_category(df, **options)
        #print(f'upd_chart fig:<{fig}>')
        return [fig]

    @app.callback(
        Output('categories', 'children'),
        Input('dropdown-categories', 'value')
    )
    def update_output(value):
        return f'Your choose: {value}'

