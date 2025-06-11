# drilldown_app.py
import os
import dash
from dash import dcc, html, dash_table, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
import plotly.graph_objects as go

import utils.sql_db_rw

from GetData import Qsfc, DrawPlot
from sql_db_rw import SqliteDB

shutdown_flag = {"exit": False}
today = date.today().isoformat()


def create_app():
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    #app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.title = "QSFC Data Visualisation"

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
                            {'label': 'Mkt Item', 'value': 'mkt_item'},
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

    app.layout = dmc.MantineProvider(

        children=dbc.Container([
            dcc.Store(id='current-level', data=0),
            dcc.Store(id='current-cat_val', data=''),

            dbc.Row([
                dbc.Col(
                    children=dmc.Flex(
                        direction="row",
                        gap="sm",
                        style={'margin-left': '10px',
                            'border': '0px groove darkblue',
                            'padding': '10px',
                            'margin': '10px',
                            'border-radius': '5px'
                        },
                        children=[
                            dmc.RadioGroup(
                                id="period-selector",
                                #label="Select period",
                                value="last_year",
                                children=[
                                    dmc.Flex(
                                        gap="xl",
                                        children=[

                                            dmc.Radio(value="last_year", label="Last Year",w=40),
                                            dmc.Radio(value="last_month", label="Last Month",w=40),
                                            dmc.Radio(value="date_range", label="Dates Range",w=80),

                                        ],
                                    )
                                ], style={'margin-top': '10px'}
                            ),


                            dmc.DatePickerInput(
                                id="date-picker-from",
                                label="From",
                                value='2021-01-01',
                                valueFormat="YYYY-MM-DD",
                                disabled=True,
                                w=120,
                            ),

                            dmc.DatePickerInput(
                                id="date-picker-upto",
                                label="To",
                                value=today,
                                valueFormat="YYYY-MM-DD",
                                disabled=True,
                                w=120,
                            ),

                            dbc.Button("Apply dates", id='apply_dates', n_clicks=0,
                                       className='mr-2',),
                            dbc.Button('Draw/Redraw Graph', id='get_data', n_clicks=0,
                                       className='mr-2'),




                        ],
                    ),
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
                        'border-radius': '5px'
                    }
                ),

            ]),
            dbc.Row([

                dbc.Col(
                    dcc.Graph(id='main-chart',
                              style={"height": "80vh"}
                              ),
                    width=12,

                ),
            ]),


        ])
    )
    
    register_callbacks(app)

    return app
    
def register_callbacks(app):

    @app.callback(
        [Output('main-chart', 'figure'),
         Output('current-level', 'data'),
         Output('current-cat_val', 'data')],
        [Input('main-chart', 'clickData'),
         Input('get_data', 'n_clicks'),
         Input('dropdown-categories', 'value'),
         Input('cb_all_when', 'value'),
         Input('cb_period', 'value'),
         Input('cb_tat_categories', 'value'),
         Input('cb_tat2_categories', 'value'),
         Input("period-selector", "value"),],
        [State('date-picker-from', 'value'),
         State('date-picker-upto', 'value'),
         State('current-level', 'data'),
         State('current-cat_val', 'data'),
         State('main-chart', 'figure'),]
        )
    # # Output('cb_period', 'style')
    def update_chart(clickData, n, ret_cat, all_when, period, tat_category, tat2_category,
                     per_sel, date_from, date_upto, level, curr_cat_val, curr_chart):

        default_fig = go.Figure()
        default_style = {'visibility': 'hidden'}
        if not n:
            #return default_fig
            pass
            #, default_style  # пустой график до нажатия

        print('\nupdate_chart','n:', n, 'ret_cat:', ret_cat, 'all_when:', all_when, 'period:', period,
              'tat_category:', tat_category,  'tat2_category:', tat2_category,
              'date_from:', date_from, 'date_upto:', date_upto, 'per_sel:', per_sel, 'level:', level,
              'curr_cat_val:', curr_cat_val,
              )

        from dash import callback_context

        triggered_lbl = ''
        triggered_x = ''
        # print("Triggered by:", callback_context.triggered)
        # print("clickData:", clickData)
        ctx = callback_context
        triggered = ctx.triggered[0]['prop_id'] if ctx.triggered else ''
        trigger_id = triggered.split('.')[0]
        if clickData:
            triggered_lbl = clickData['points'][0]['label']
            triggered_x = clickData['points'][0]['x']
            print("triggered_lbl:", triggered_lbl, "triggered_x:", triggered_x)
        print("triggered:", triggered, "trigger_id:", trigger_id)

        fig = None
        new_level = level
        new_cat_val = curr_cat_val

        cb_period_vis = {'visibility': 'hidden'} if all_when=="all" else {'visibility': 'visible'}

        if triggered == 'main-chart.clickData':
            if level == 0:
                new_level = 1
                new_cat_val = triggered_lbl
            elif level == 1:
                new_level = 2
                new_cat_val = triggered_lbl
            elif level == 2:
                new_level = 3
                new_cat_val = triggered_lbl

        else:
            new_level = 0
            new_cat_val = ret_cat
        print(f'triggered:{triggered} level:{level} new_level:{new_level} new_cat_val:{new_cat_val} ')

        if per_sel == 'date_range':
            pass
        elif per_sel == 'last_month':
            date_from = date.today() - timedelta(days=30)
            date_upto = date.today()
        elif per_sel == 'last_year':
            date_from = date.today() - timedelta(days=365)
            date_upto = date.today()


        if level == 3 or (level==2 and tat2_category == 'None') or (level==1 and tat_category == 'None'):
            return curr_chart, new_level, new_cat_val


        sql_obj = SqliteDB()
        sql_db = sql_obj.db_name(os.path.dirname(os.path.abspath(__file__)), 'db_qsfc.db')
        #sql_db = os.path.abspath(str(os.path.join(os.path.abspath(__file__), 'db_qsfc.db')))
        #sql_obj.db = sql_db
        dp = DrawPlot()
        options = {
            'cat': ret_cat,
            'tit': 'Total RMAs',
            'xaxis_tit': f'{ret_cat.upper()}',
            'yaxis_tit': 'Quantity',
            'chart_type': 'bar',
            'drill_plot_only' : True,
        }

        fig_type = ''
        if triggered == 'main-chart.clickData':
            options['cat'] = tat_category
            options['tit'] = f"{ret_cat.replace('_', ' ').upper()} {triggered_lbl} per {tat_category.replace('_', ' ').upper()}"

            if tat_category=='1nff' or tat_category=='1doa':
                options['tit'] = f"All {tat_category.replace('_', ' ').upper()} of {triggered_lbl.replace('_', ' ').upper()}"
                options['xaxis_tit'] = f'{triggered_lbl}'
                print('main 1')
                df = sql_obj.read_table('RMA', date_from, date_upto, ret_cat=[tat_category],
                                    cat=ret_cat, cat_val=[triggered_lbl],
                                    cat2=tat_category, cat2_val="1")
                fig_type = 'category'
            else:
                options['xaxis_tit'] = f"{tat_category.replace('_', ' ').upper()}"
                if new_level == 1:
                    print('main 2.1')
                    if tat_category != 'None':
                        print('main 2.1.1')
                        df = sql_obj.read_table('RMA', date_from, date_upto, ret_cat=[tat_category], cat=ret_cat,
                                cat_val=[triggered_lbl])
                        fig_type = 'category'
                    else:
                        print('main 2.1.2')
                        if all_when == 'all':
                            print('main 2.1.2.1')
                            df = sql_obj.read_table('RMA', date_from, date_upto, ret_cat=[ret_cat], cat=ret_cat,
                                    cat_val=[triggered_lbl])
                            options['cat'] = ret_cat
                            fig_type = 'cat_day'
                        elif all_when == 'when':
                            print('main 2.1.2.2')
                            date_from = new_cat_val
                            date_obj = datetime.strptime(date_from, '%Y-%m-%d')
                            if period == 'month':
                                new_date = date_obj + relativedelta(months=1)
                            elif period == 'week':
                                new_date = date_obj + relativedelta(weeks=1)
                            date_upto = new_date.strftime('%Y-%m-%d')
                            options['cat'] = [ret_cat][0]
                            df = sql_obj.read_table('RMA', date_from, date_upto, ret_cat=[ret_cat])
                            print(f'df:{df}')
                            fig_type = 'category'


                elif new_level == 2:
                    print('main 2.2')
                    if tat2_category != 'None':
                        print('main 2.2.1')
                        options['cat'] = tat2_category
                        df = sql_obj.read_table('RMA', date_from, date_upto, ret_cat=[tat2_category],
                                            cat=[tat_category][0], cat_val=new_cat_val,
                                            cat2=[tat_category][0], cat2_val=[triggered_lbl],)
                        # print(f'df:{df}')
                        fig_type = 'category'
                    else:
                        print('main 2.2.2')
                        options['cat'] = tat_category
                        options['tit'] = f'for {new_cat_val} {tat_category.upper()}:{triggered_lbl}'
                        df = sql_obj.read_table('RMA', date_from, date_upto, ret_cat=[tat_category],
                                            cat=tat_category, cat_val=new_cat_val,
                                            )
                        # print(f'df:{df}')
                        fig_type = 'cat_day'
                elif new_level == 3:
                    print('main 2.3')
                    print('main 2.3.2')
                    options['cat'] = tat2_category
                    options['tit'] = f'for {new_cat_val} {tat_category.upper()}:{triggered_lbl}'
                    df = sql_obj.read_table('RMA', date_from, date_upto, ret_cat=[tat2_category],
                                        cat=tat_category, cat_val=curr_cat_val,
                                        cat2=tat2_category, cat2_val=new_cat_val, )
                    # print(f'df:{df}')
                    fig_type = 'cat_day'
            print('main fig_type: ', fig_type)
            if fig_type == 'category':
                fig = dp.by_category(df, **options)
            elif fig_type == 'cat_day':
                fig = dp.by_cat_day(df, **options)


        else:
            if all_when=='when':
                print('not_main 3.1')
                df = sql_obj.read_period_counts('RMA', date_from, date_upto, period)

                #fig = dp.by_cat_day(df, **options)
                options['period'] = period
                options['tit'] = f'RMAs per {period}'
                options['xaxis_tit'] = ''
                fig_type = 'period'
                fig = dp.by_period(df, **options)
            elif all_when=='all':
                print('not_main 3.2')
                options['tit'] = f'RMAs per {ret_cat.upper()}'
                if ret_cat=='nff' or ret_cat=='doa':
                    df = sql_obj.read_table('RMA', date_from, date_upto, ret_cat=[ret_cat], cat=[ret_cat][0], cat_val='1')
                else:
                    df = sql_obj.read_table('RMA', date_from, date_upto, ret_cat=[ret_cat])
                fig_type = 'category'
                fig = dp.by_category(df, **options)
                pass
        # if fig is None:
        #    df = sql.read_table('RMA', date_from, date_upto, ret_cat=[ret_cat])
        #    fig = dp.by_category(df, **options)
        #print(f'upd_chart fig:<{fig}>')
        print(f"Returning new_level:{new_level}, new_cat_val:{new_cat_val}")
        return fig,  new_level, new_cat_val
        # , cb_period_vis

    @app.callback(
        Output('cb_period', 'style'),
        [Input('cb_all_when', 'value')]
    )
    def update_cb_period_style(all_when):
        cb_period_vis = {'visibility': 'hidden'} if all_when == "all" else {'visibility': 'visible'}
        print("update_cb_period_styleReturning:",  cb_period_vis)
        return cb_period_vis

    @app.callback(
        Output("date-picker-from", "disabled"),
        Output("date-picker-upto", "disabled"),
        Input("period-selector", "value"),
    )
    def toggle_datepickers(selected):
        if selected == "date_range":
            return False, False
        return True, True

if __name__ == "__main__":
    app = create_app()
    try:
        app.run(port=8081, debug=True, use_reloader=True)  # Use reloader=False to avoid issues with reloading
    except KeyboardInterrupt:
        print("Server stopped by KeyboardInterrupt")
        exit()
        