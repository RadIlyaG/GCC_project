import dash

from dash import dcc, html, dash_table, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
import plotly.graph_objects as go


def create_app():
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    #app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.title = "TCC-QSFC Data Visualisation"

    today = date.today().isoformat()
    cb_categories_options = [
        {'label': 'Product Line', 'value': 'product_line'},
        {'label': 'Mkt Item', 'value': 'mkt_item'},
    ]
    cb_categories_options.sort(key=lambda x: x['label'])

    app.layout = dmc.MantineProvider(
        children=dbc.Container([
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
                                # label="Select period",
                                value="last_year",
                                children=[
                                    dmc.Flex(
                                        gap="xl",
                                        children=[

                                            dmc.Radio(value="last_year", label="Last Year", w=40),
                                            dmc.Radio(value="last_month", label="Last Month", w=40),
                                            dmc.Radio(value="date_range", label="Dates Range", w=80),

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
                                       className='mr-2', ),
                            dbc.Button('Draw Graph', id='get_data', n_clicks=0,
                                       className='mr-2'),



                        ],
                    ),
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
                    ]),
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
        ]),
    )

    register_callbacks(app)
    return app

def register_callbacks(app):
    @app.callback(
        Output('main-chart', 'figure'),
        [Input('main-chart', 'clickData'),
         Input('get_data', 'n_clicks'),
         Input('dropdown-categories', 'value'),
         Input("period-selector", "value"), ],
        [State('date-picker-from', 'value'),
         State('date-picker-upto', 'value'),
         State('main-chart', 'figure'), ]
    )
    # # Output('cb_period', 'style')
    def update_chart(clickData, n, ret_cat, per_sel,
                     date_from, date_upto, curr_chart):
        fig = curr_chart
        return fig

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
    try:
        applic = create_app()
        applic.run(port=8082, debug=True, use_reloader=True)  # Use reloader=False to avoid issues with reloading
    except KeyboardInterrupt:
        print("Server stopped by KeyboardInterrupt")
        exit()