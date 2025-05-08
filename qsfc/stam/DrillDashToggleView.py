import dash
from dash import dcc, html, dash_table, Input, Output, State, callback_context
import plotly.graph_objects as go
from collections import defaultdict
import datetime

# Sample data
data = [
    {'date': datetime.datetime(2025, 4, 1), 'customer': 'Alice', 'product': 'Apples', 'quantity': 2, 'price': 3.5},
    {'date': datetime.datetime(2025, 4, 2), 'customer': 'Alice', 'product': 'Bananas', 'quantity': 3, 'price': 2.0},
    {'date': datetime.datetime(2025, 4, 1), 'customer': 'Bob', 'product': 'Cars', 'quantity': 2, 'price': 30000},
    {'date': datetime.datetime(2025, 4, 3), 'customer': 'Bob', 'product': 'Bananas', 'quantity': 1, 'price': 2.5},
    {'date': datetime.datetime(2025, 4, 3), 'customer': 'Alice', 'product': 'Cars', 'quantity': 1, 'price': 32000},
]

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H2("Customer Purchases Dashboard"),

    dcc.RadioItems(
        id='view-mode',
        options=[
            {'label': 'Combined View', 'value': 'combined'},
            {'label': 'Split View', 'value': 'split'}
        ],
        value='combined',
        labelStyle={'display': 'inline-block', 'margin-right': '10px'}
    ),

    dcc.Graph(id='main-chart'),

    html.Button("Back", id='back-button'),

    html.Div(
        dash_table.DataTable(
            id='raw-data-table',
            style_table={'overflowX': 'auto'},
            page_size=10
        ),
        id='table-container'
    ),

    dcc.Store(id='current-level', data='customer'),
    dcc.Store(id='selected-customer'),
    dcc.Store(id='selected-product'),
    dcc.Store(id='data-store', data=data),
])

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
    Input('view-mode', 'value'),
    State('current-level', 'data'),
    State('selected-customer', 'data'),
    State('selected-product', 'data'),
    State('data-store', 'data'),
    prevent_initial_call=True
)


def update_chart(clickData, n_clicks, level, selected_customer, selected_product, data):
    ctx = callback_context

    triggered = ctx.triggered[0]['prop_id'] if ctx.triggered else None

    fig = go.Figure()
    table_data = []
    columns = []
    back_style = {'display': 'none'}

    if level == 'customer':
        customer_totals = defaultdict(int)
        for row in data:
            customer_totals[row['customer']] += row['quantity']

        fig.add_trace(go.Bar(
            x=list(customer_totals.keys()),
            y=list(customer_totals.values()),
            text=list(customer_totals.values()),
            textposition='auto'
        ))
        fig.update_layout(title='Purchases by Customer')

        table_data = data
        columns = [{'name': k, 'id': k} for k in data[0].keys()]

        if triggered == 'main-chart.clickData':
            selected_customer = clickData['points'][0]['x']
            level = 'product'

    elif level == 'product':
        back_style = {'display': 'inline-block'}
        product_totals = defaultdict(int)
        for row in data:
            if row['customer'] == selected_customer:
                product_totals[row['product']] += row['quantity']

        fig.add_trace(go.Bar(
            x=list(product_totals.keys()),
            y=list(product_totals.values()),
            text=list(product_totals.values()),
            textposition='auto'
        ))
        fig.update_layout(title=f"{selected_customer}'s Purchases by Product")

        table_data = [row for row in data if row['customer'] == selected_customer]
        columns = [{'name': k, 'id': k} for k in table_data[0].keys()] if table_data else []

        if triggered == 'main-chart.clickData':
            selected_product = clickData['points'][0]['x']
            level = 'time'

        if triggered == 'back-button.n_clicks':
            level = 'customer'
            selected_customer = None

    elif level == 'time':
        back_style = {'display': 'inline-block'}
        date_totals = defaultdict(float)
        for row in data:
            if row['customer'] == selected_customer and row['product'] == selected_product:
                date_totals[row['date']] += row['price']

        fig.add_trace(go.Bar(
            x=list(date_totals.keys()),
            y=list(date_totals.values()),
            text=[f"${v:.2f}" for v in date_totals.values()],
            textposition='auto'
        ))
        fig.update_layout(title=f"{selected_customer}'s '{selected_product}' Prices Over Time")

        table_data = [row for row in data if row['customer'] == selected_customer and row['product'] == selected_product]
        columns = [{'name': k, 'id': k} for k in table_data[0].keys()] if table_data else []

        if triggered == 'back-button.n_clicks':
            level = 'product'
            selected_product = None

    #return fig, back_style, table_data, columns, {'display': 'block'}
    return fig, back_style, table_data, columns, {'display': 'block'}, level, selected_customer, selected_product


if __name__ == '__main__':
    app.run(debug=True)
