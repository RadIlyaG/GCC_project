# drilldown_app.py
import dash
from dash import dcc, html, dash_table, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
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

    # {'label': 'None', 'value': 'None'},
    # {'label': 'Customer', 'value': 'customers_name'},
    # {'label': 'NFF', 'value': 'nff'},
    # {'label': 'DOA', 'value': 'doa'},
    # {'label': 'Failure Description', 'value': 'failure_desc'},
    # {'label': 'Location', 'value': 'location'},
    # {'label': 'Date code', 'value': 'date_code'},
    # {'label': 'Arrive date not empty', 'value': 'arrive_date'},
    cb_categories_options = [
                            {'label': 'NFF', 'value': 'nff'},
                            {'label': 'DOA', 'value': 'doa'},
                            {'label': 'Product Line', 'value': 'product_line'},
                            {'label': 'Catalog', 'value': 'catalog'},
                            {'label': 'CSL', 'value': 'csl'},
                            {'label': 'Customer', 'value': 'customers_name'},
                            {'label': 'Fail Desc.', 'value': 'failure_desc'},
                            {'label': 'Location', 'value': 'location'},
                            {'label': 'Date code', 'value': 'date_code'},
                            {'label': 'RAD part', 'value': 'rad_part'},
                        ]
    cb_categories_options.sort(key=lambda x: x['label'])
    cb_tatcategories_options = [{'label': 'None', 'value': 'None'},]
    cb_tatcategories_options.extend(cb_categories_options)



    app.layout = html.Div([
        #dcc.Graph(figure=fig),
        dbc.Row([
            # dbc.Col(dmc.MantineProvider(
                # theme={
                    # "colorScheme": "light",
                    # "fontFamily": "Arial, sans-serif",
                # },
                # children=html.Div([
                    # dmc.DatePickerInput(
                        # id="date-picker-from",
                        # label="FROM date: ",
                        # placeholder="Select a date...",
                        # #value=None,
                        # valueFormat="YYYY-MM-DD",  # e.g., May 26, 2025
                        # firstDayOfWeek=0,
                        # clearable=False,
                        # size="sm",
                        # value='2021-01-01',
                        # w=120,
                        # className="shift-input"
                    # ),
                    # dmc.DatePickerInput(
                        # id="date-picker-upto",
                        # label="UPTO date",
                        # placeholder="Select a date...",
                        # # value=None,
                        # valueFormat="YYYY-MM-DD",  # e.g., May 26, 2025
                        # firstDayOfWeek=0,
                        # clearable=False,
                        # size="sm",
                        # value=date.today().strftime("%Y-%m-%d"),
                        # w=100,
                        # className="shift-input"
                    # ),
                # ])
            # )
            # ),
            dbc.Col([
                html.Label("FROM date: ", style={'font-size': '16px'}),
                dcc.DatePickerSingle(
                    id='date-picker-from',
                    date='2021-01-01',
                    display_format='YYYY-MM-DD',
                    style={
                        'width': '130px',
                    }
                )
            ], width="auto",
            ),
            dbc.Col([
                html.Label("UPTO date: ", style={'font-size': '16px'}),
                dcc.DatePickerSingle(
                    id='date-picker-upto',
                    date=date.today().strftime("%Y-%m-%d"),
                    display_format='YYYY-MM-DD',
                    style={
                       'width': '130px',
                    }
                )
            ], width="auto",
            ),

            dbc.Col(
                dbc.Button("apply dates", id='apply_dates', n_clicks=0,
                           className='mr-2'),
                width=1,
            ),

            dbc.Col(
                html.Div([
                    dcc.Dropdown(
                        id='cb_all_when',
                        options=[
                            {'label': 'Per Category', 'value': 'all'},
                            {'label': 'Per Date', 'value': 'when'},
                        ],
                        value='all',  # default value
                        clearable=False,  # can't clear the entry
                        multi=False
                    ),
                    html.Br(),
                    dcc.Dropdown(
                        id='cb_period',
                        options=[
                            {'label': 'Per Month', 'value': 'month'},
                            {'label': 'Per Week', 'value': 'week'},
                        ],
                        value='month',  # default value
                        clearable=False,  # can't clear the entry
                        multi=False,
                        style={'visibility': 'hidden'}
                    ),
                ]),
                width=2, style={
                    'border': '2px groove gray',
                    'padding': '10px',
                    'margin': '10px'
                }
            ),
            dbc.Col(
                html.Div([
                    dcc.Dropdown(
                        id='dropdown-categories',
                        options=cb_categories_options,
                        value='product_line',  # default value
                        clearable=False,  # can't clear the entry
                        multi=False
                    ),
                    html.Label("Drill down by: ", style={'font-size': '16px'}),
                    dcc.Dropdown(
                        id='cb_tat_categories',
                        options=cb_tatcategories_options,
                        value='None',  # default value
                        clearable=False,  # can't clear the entry
                        multi=False
                    ),
                    html.Label("Drill even deeply: ", style={'font-size': '16px'}),
                    dcc.Dropdown(
                        id='cb_tat2_categories',
                        options=cb_tatcategories_options,
                        value='None',  # default value
                        clearable=False,  # can't clear the entry
                        multi=False
                    ),
                ]),
                width=2, style={
                    'border': '2px groove darkblue',
                    'padding': '10px',
                    'margin': '10px',
                    'border-radius' : '5px'
                }
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
                dcc.Graph(id='main-chart',
                          style={"height": "80vh"}
                          ),
                width=11,

            ),
        ]),
        html.Button("Back", id='back-button', style={'display': 'none'}),


    ])
    
    register_callbacks(app)

    return app
    
def register_callbacks(app):
    @app.callback(
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
            #return 'Select a date to see it displayed here'
            pass
        else:
            #print(f'3, {string_prefix}')
            #return ''  #string_prefix
            pass

    @app.callback(
        Output('main-chart', 'figure'),
        [Input('main-chart', 'clickData'),
         Input('get_data', 'n_clicks'),
         Input('dropdown-categories', 'value'),
         Input('cb_all_when', 'value'),
         Input('cb_period', 'value'),
         Input('cb_tat_categories', 'value')],
        [State('date-picker-from', 'date'),
         State('date-picker-upto', 'date')]
        )
    # Output('cb_period', 'style')
    def update_chart(clickData, n, ret_cat, all_when, period, tat_category, date_from, date_upto):

        default_fig = go.Figure()
        default_style = {'visibility': 'hidden'}
        if not n:
            #return default_fig
            pass
            #, default_style  # пустой график до нажатия

        print('\nupdate_chart','n:', n, 'ret_cat:', ret_cat, 'all_when:', all_when, 'period:', period,
              'tat_category:', tat_category,  'date_from:', date_from,  'date_upto:', date_upto,
              )

        from dash import callback_context

        triggered_lbl = ''
        print("Triggered by:", callback_context.triggered)
        print("clickData:", clickData)
        ctx = callback_context
        triggered = ctx.triggered[0]['prop_id'] if ctx.triggered else ''
        trigger_id = triggered.split('.')[0]
        if clickData:
            triggered_lbl = clickData['points'][0]['label']
            print("triggered_lbl:", triggered_lbl)
        print("triggered:", triggered, "trigger_id:", trigger_id)

        fig = None

        cb_period_vis = {'visibility': 'hidden'} if all_when=="all" else {'visibility': 'visible'}

        sql = SqliteDB()
        dp = DrawPlot()
        options = {
            'cat': ret_cat,
            'tit': 'Total RMAs',
            'xaxis_tit': f'{ret_cat.upper()}',
            'yaxis_tit': 'Quantity',
            'chart_type': 'bar',
            'drill_plot_only' : True,
        }
        if triggered == 'main-chart.clickData':
            options['cat'] = tat_category
            options['tit'] = f"{ret_cat.replace('_', ' ').upper()} {triggered_lbl} per {tat_category.replace('_', ' ').upper()}"

            if tat_category=='nff' or tat_category=='doa':
                options['tit'] = f"All {tat_category.replace('_', ' ').upper()} of {triggered_lbl.replace('_', ' ').upper()}"
                options['xaxis_tit'] = f'{triggered_lbl}'
                df = sql.read_table('RMA', date_from, date_upto, ret_cat=[tat_category],
                                    cat=ret_cat, cat_val=[triggered_lbl],
                                    cat2=tat_category, cat2_val="1")
            else:
                options['xaxis_tit'] = f"{tat_category.replace('_', ' ').upper()}"
                df = sql.read_table('RMA', date_from, date_upto, ret_cat=[tat_category], cat=ret_cat,
                                cat_val=[triggered_lbl])
            fig = dp.by_category(df, **options)
            # if ret_cat == 'product_line':
            #     if tat_category == 'customers_name':
            #         options['cat'] = tat_category
            #         options['tit'] = f'{triggered_lbl} per {tat_category}',
            #         df = sql.read_table('RMA', date_from, date_upto, ret_cat=[tat_category], cat=ret_cat, cat_val=[triggered_lbl])
            #         fig = dp.by_category(df, **options)
            #     if tat_category == 'nff':
            #         options['cat'] = tat_category
            #         options['tit'] = f'All {triggered_lbl} of {tat_category}',
            #         df = sql.read_table('RMA', date_from, date_upto, ret_cat=[tat_category], cat=ret_cat, cat_val=[triggered_lbl])
            #         fig = dp.by_category(df, **options)
            # if ret_cat == 'catalog':
            #     if tat_category == 'customers_name':
            #         options['cat'] = tat_category
            #         options['tit'] = f'{triggered_lbl} per {tat_category}',
            #         df = sql.read_table('RMA', date_from, date_upto, ret_cat=[tat_category], cat=ret_cat, cat_val=[triggered_lbl])
            #         fig = dp.by_category(df, **options)
            #     if tat_category == 'nff':
            #         options['cat'] = tat_category
            #         options['tit'] = f'All {triggered_lbl} of {tat_category}',
            #         df = sql.read_table('RMA', date_from, date_upto, ret_cat=[tat_category], cat=ret_cat, cat_val=[triggered_lbl])
            #         fig = dp.by_category(df, **options)

        else:
            if all_when=='when':
                df = sql.read_period_counts('RMA', date_from, date_upto, period)
                #fig = dp.by_cat_day(df, **options)
                options['period'] = period
                options['tit'] = f'RMAs per {period}'
                options['xaxis_tit'] = ''
                fig = dp.by_period(df, **options)
            elif all_when=='all':
                options['tit'] = f'RMAs per {ret_cat.upper()}'
                if ret_cat=='nff' or ret_cat=='doa':
                    df = sql.read_table('RMA', date_from, date_upto, ret_cat=[ret_cat], cat=[ret_cat][0], cat_val='1')
                else:
                    df = sql.read_table('RMA', date_from, date_upto, ret_cat=[ret_cat])
                fig = dp.by_category(df, **options)
                pass
        # if fig is None:
        #    df = sql.read_table('RMA', date_from, date_upto, ret_cat=[ret_cat])
        #    fig = dp.by_category(df, **options)
        #print(f'upd_chart fig:<{fig}>')
        print("Returning:", type(fig), cb_period_vis)
        return fig
        # , cb_period_vis

    @app.callback(
        Output('cb_period', 'style'),
        [Input('cb_all_when', 'value')]
    )
    def update_cb_period_style(all_when):
        cb_period_vis = {'visibility': 'hidden'} if all_when == "all" else {'visibility': 'visible'}
        print("update_cb_period_styleReturning:",  cb_period_vis)
        return cb_period_vis

app = create_app('data')

if __name__ == "__main__":
    #webbrowser.open("http://127.0.0.1:8050")
    app.run(port=8081, debug=True, use_reloader=True)