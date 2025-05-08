# drilldown_app.py
import dash
from dash import dcc, html, dash_table, Input, Output, State, callback_context
import os
import signal
import plotly.graph_objects as go
from collections import defaultdict
import time
import threading
import requests

def create_app(data):
    app = dash.Dash(__name__)
    app.title = "Drilldown Chart App"

    app.layout = html.Div([
        html.H1("Drilldown Dashboard"),
        dcc.Graph(id='main-chart'),
        html.Button("Exit", id="exit-button", n_clicks=0),
        html.Button("Back", id='back-button', style={'display': 'none'}),
        html.Div(id='exit-message', style={'marginTop': '20px', 'color': 'red', 'fontWeight': 'bold'}),
        dcc.Store(id='current-level', data='customer'),
        dcc.Store(id='selected-customer'),
        dcc.Store(id='selected-product'),
        dcc.Store(id='data-store', data=data),
        html.Div(id='table-container', children=[
            dash_table.DataTable(id='raw-data-table')
        ], style={'display': 'block'}),
    ])

    register_callbacks(app)

    return app

def register_callbacks(app):
    @app.callback(
        Output('main-chart', 'figure'),
        Output('back-button', 'style'),
        Output('raw-data-table', 'data'),
        Output('raw-data-table', 'columns'),
        Output('table-container', 'style'),
        Output('current-level', 'data'),
        Output('selected-customer', 'data'),
        Output('selected-product', 'data'),
        Input('main-chart', 'clickData'),
        Input('back-button', 'n_clicks'),
        State('current-level', 'data'),
        State('selected-customer', 'data'),
        State('selected-product', 'data'),
        State('data-store', 'data'),
    )
    def update_chart(clickData, n_clicks, level, selected_customer, selected_product, data):
        from collections import defaultdict
        from dash import callback_context
        import plotly.graph_objects as go

        print("Triggered by:", callback_context.triggered)
        print("clickData:", clickData)

        # Инициализация значений
        ctx = callback_context
        triggered = ctx.triggered[0]['prop_id'] if ctx.triggered else ''

        fig = go.Figure()
        back_style = {'display': 'none'}
        new_level = level
        new_selected_customer = selected_customer
        new_selected_product = selected_product
        filtered_data = data

        # === 1. Обработка переходов вперёд при клике на графике ===
        if triggered == "main-chart.clickData":
            if level == 'customer':
                new_selected_customer = clickData['points'][0]['x']
                new_level = 'product'
            elif level == 'product':
                new_selected_product = clickData['points'][0]['x']
                new_level = 'time'

        # === 2. Обработка переходов назад ===
        if triggered == "back-button.n_clicks":
            if level == 'time':
                new_level = 'product'
                new_selected_product = None
            elif level == 'product':
                new_level = 'customer'
                new_selected_customer = None

        # === 3. Отрисовка графика и таблицы в зависимости от текущего уровня ===
        if new_level == 'customer':
            customer_totals = defaultdict(int)
            for row in data:
                customer_totals[row['customer']] += row['quantity']
            fig.add_trace(go.Bar(
                x=list(customer_totals.keys()),
                y=list(customer_totals.values()),
                text=list(customer_totals.values()),
                textposition='auto'
            ))
            fig.update_layout(title="Total Purchases by Customer")
            filtered_data = data  # показываем все данные
            back_style = {'display': 'none'}  # кнопка назад не показывается

        elif new_level == 'product':
            filtered_data = [row for row in data if row['customer'] == new_selected_customer]
            product_totals = defaultdict(int)
            for row in filtered_data:
                product_totals[row['product']] += row['quantity']
            fig.add_trace(go.Bar(
                x=list(product_totals.keys()),
                y=list(product_totals.values()),
                text=list(product_totals.values()),
                textposition='auto'
            ))
            fig.update_layout(title=f"Products bought by {new_selected_customer}")
            back_style = {'display': 'inline-block'}

        elif new_level == 'time':
            filtered_data = [
                row for row in data if
                row['customer'] == new_selected_customer and row['product'] == new_selected_product
            ]
            filtered_data.sort(key=lambda x: x['date'])
            fig.add_trace(go.Scatter(
                x=[row['date'] for row in filtered_data],
                y=[row['price'] for row in filtered_data],
                mode='lines+markers+text',
                text=[f"${row['price']}" for row in filtered_data],
                textposition='top center'
            ))
            fig.update_layout(title=f"{new_selected_product} prices over time for {new_selected_customer}")
            back_style = {'display': 'inline-block'}

        # === 4. Построение таблицы ===
        table_columns = [{"name": k, "id": k} for k in filtered_data[0].keys()] if filtered_data else []

        return fig, back_style, filtered_data, table_columns, {
            'display': 'block'}, new_level, new_selected_customer, new_selected_product

    # Create a shutdown function that stops the server

    @app.callback(
        Output('exit-message', 'children'),
        Input('exit-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def exit_app(n_clicks):
        shutdown_message = "Server stopped. You can close this tab now."
        import threading
        threading.Timer(1.0, lambda: os._exit(0)).start()

        return shutdown_message
        # if n_clicks > 0:
        #     # Send a request to the shutdown route to stop the server
        #     import requests
        #     # requests.post("http://127.0.0.1:8050/shutdown")  # Trigger shutdown by hitting the route
        #     threading.Thread(target=delayed_shutdown, daemon=True).start()
        # return n_clicks

    def delayed_shutdown():
        time.sleep(1)  # Let the response finish
        try:
            requests.post("http://127.0.0.1:8050/shutdown")
        except Exception as e:
            print("Server already shut down.")

    @app.server.route("/shutdown", methods=["POST"])
    def shutdown():
        """Shut down the server gracefully."""
        os.kill(os.getpid(), signal.SIGINT)
        return 'Server shutting down...'
