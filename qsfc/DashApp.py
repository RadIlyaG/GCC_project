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

shutdown_flag = {"exit": False}

def create_app(data):
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    #app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.title = "QSFC Data Vizualisation"

    app.layout = html.Div([
        #dcc.Graph(figure=fig),
        dbc.Row([
            dbc.Col(
                html.H1("QSFC Data"),
            ),
            dbc.Col(
                html.H4("by Dash system")
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
                    # dcc.DatePickerRange(
                    #     id='my-date-picker-range',
                    #     #min_date_allowed=date(1995, 8, 5),
                    #     #max_date_allowed=date(2995, 8, 5), #date.today(),
                    #     initial_visible_month=date(2021, 1, 1), #date.today(),
                    #     end_date=date.today().strftime("%d/%b/%Y"),
                    #     start_date=date(2021, 1, 1),
                    #     #month_format='DD MMMM YYYY',
                    #     start_date_placeholder_text=date.today(),
                    #     end_date_placeholder_text=date.today().strftime("%d/%b/%Y"),
                    #     display_format='DD/MM/Y'
                    # ),
                    # html.Div(id='output-container-date-picker-range'),
                    html.Div("FROM date"),
                    dcc.DatePickerSingle(
                        id='date-picker-from',
                        #date=(date.today() - timedelta(days=365)).strftime("%d/%b/%Y"),
                        display_format='YYYY-MM-DD',
                        #date=date.today() - timedelta(days=365),
                        date=date.today() - timedelta(days=30),
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
                width=5,
            ),
        ], class_name='row_style',
        ),
        dbc.Row([
            dbc.Col(
                dbc.Button("Get data from QSFC DB", id='get_data', n_clicks=0,
                           className='mr-2'),
                width=1,
            ),
            dbc.Col(
                #html.Div(dcc.Graph(figure=fig), id='plot_place'),
                dcc.Graph(id='plot_1',
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
        print('n:', n, start_date, end_date)
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
            print(f'1, {string_prefix}')
        if end_date is not None:
            try:
                end_date_object = date.fromisoformat(end_date)
            except ValueError:
                string_prefix = string_prefix + 'End Date: ' + end_date
            else:
                end_date_string = end_date_object.strftime('%d/%m/%Y')
                string_prefix = string_prefix + 'End Date: ' + end_date_string
            #string_prefix = string_prefix + 'End Date: ' + end_date
            print(f'2, {string_prefix}')
        if len(string_prefix) == len('You have selected: '):
            return 'Select a date to see it displayed here'
        else:
            print(f'3, {string_prefix}')
            return string_prefix

    @app.callback(
        [Output('plot_1', 'figure')],
        [Input('get_data', 'n_clicks')],
        [State('date-picker-from', 'date'),
         State('date-picker-upto', 'date')]
        )
    def update_chart(n, start_date, end_date):
        if not n:
            return [go.Figure()]  # пустой график до нажатия
        print('n:', n, 'start_date:', start_date)
        from GetData import Qsfc, DrawPlot
        qsfc = Qsfc()
        qsfc.print_rtext = True
        res_list = []
        #df = qsfc.get_data_from_qsfc('Prod', "11/02/2025", "13/02/2025")
        formatted_start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%d/%m/%Y')
        formatted_end_date   = datetime.strptime(end_date, '%Y-%m-%d').strftime('%d/%m/%Y')
        print('n:', n, 'formatted_start_date:', formatted_start_date, 'formatted_end_date', formatted_end_date)
        df = qsfc.get_data_from_qsfc('RMA', formatted_start_date, formatted_end_date)
        dp= DrawPlot()
        dp.data = df
        dp.parse_date_from_str_into_datetime()
        #fig = dp.by_string(df, 'tested_catalog', 'Prod by tested_catalog', 'Quantity', 'cat')
        options = {'chart_type': 'pie'}
        fig = dp.by_string(df, 'customers_name', 'RMAs by customer', 'Quantity',
                           'Customer', **options)
        return [fig]

        #df = qsfc.get_data_from_qsfc('Prod', "11/02/2025", "13/02/2025")
        for dicti in df:
            pass #print(dicti['open_date'])


        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[row['quantity'] for row in df], #'open_date'
            y=[row['tested_catalog'] for row in df], #'product_line'
            mode='markers'
        ))
        return [fig]


