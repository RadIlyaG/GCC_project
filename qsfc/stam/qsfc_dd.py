import dash
from dash import dcc, html, Input, Output, State
from dash import dash_table
import plotly.graph_objects as go
from datetime import datetime
from collections import defaultdict

# Sample Data
data = [
    {'date': '2025-04-01', 'customer': 'Alice', 'product': 'Apples', 'quantity': 2, 'price': 3.5},
    {'date': '2025-04-02', 'customer': 'Alice', 'product': 'Bananas', 'quantity': 3, 'price': 2.0},
    {'date': '2025-04-01', 'customer': 'Bob', 'product': 'Cars', 'quantity': 1, 'price': 20000},
    {'date': '2025-04-02', 'customer': 'Bob', 'product': 'Cars', 'quantity': 2, 'price': 21000},
    {'date': '2025-04-03', 'customer': 'Alice', 'product': 'Cars', 'quantity': 1, 'price': 19500},
    {'date': '2025-04-03', 'customer': 'Bob', 'product': 'Bananas', 'quantity': 5, 'price': 1.8},
]


# Convert dates to datetime
for row in data:
    row['date'] = datetime.strptime(row['date'], "%Y-%m-%d")

app = dash.Dash(__name__)
app.title = "Customer Drilldown"
server = app.server

app.layout = html.Div([
    html.H2("📦 Customer Purchase Dashboard"),
    html.Button("⬅ Back", id='back-button', n_clicks=0, style={"display": "none"}),
    dcc.Graph(id='main-chart'),
    dcc.Store(id='current-level', data='customer'),  # 'customer', 'product', 'time'
    dcc.Store(id='selected-customer'),
    dcc.Store(id='selected-product'),
    dash_table.DataTable(
        id='raw-data-table',
        columns=[],  # filled dynamically
        data=[],
        style_table={'overflowX': 'auto', 'maxHeight': '400px', 'overflowY': 'scroll'},
        style_cell={'textAlign': 'left', 'padding': '6px'},
        style_header={'backgroundColor': '#f0f0f0', 'fontWeight': 'bold'},
        sort_action='native',
        filter_action='native',
        page_action='native',
        page_size=10,  # show 10 rows at a time
    ),
])

# Update graph based on current level
@app.callback(
    Output('main-chart', 'figure'),
    Output('back-button', 'style'),
    Input('main-chart', 'clickData'),
    Input('back-button', 'n_clicks'),
    State('current-level', 'data'),
    State('selected-customer', 'data'),
    State('selected-product', 'data')
)
def update_chart(clickData, back_clicks, level, customer, product):
    ctx = dash.callback_context
    triggered = ctx.triggered[0]['prop_id']

    # Handle navigation logic
    if triggered == "main-chart.clickData":
        if level == 'customer':
            customer = clickData['points'][0]['x']
            level = 'product'
        elif level == 'product':
            product = clickData['points'][0]['x']
            level = 'time'
    elif triggered == "back-button.n_clicks":
        if level == 'product':
            level = 'customer'
            customer = None
        elif level == 'time':
            level = 'product'
            product = None

    # Generate appropriate chart
    if level == 'customer':
        grouped = defaultdict(int)
        for row in data:
            grouped[row['customer']] += row['quantity']
        fig = go.Figure(data=[
            go.Bar(x=list(grouped.keys()), y=list(grouped.values()), textposition='auto')
        ])
        fig.update_layout(title="Total Purchases by Customer")
        back_style = {"display": "none"}

    elif level == 'product':
        grouped = defaultdict(int)
        for row in data:
            if row['customer'] == customer:
                grouped[row['product']] += row['quantity']
        fig = go.Figure(data=[
            go.Bar(x=list(grouped.keys()), y=list(grouped.values()), textposition='auto')
        ])
        fig.update_layout(title=f"Products bought by {customer}")
        back_style = {"display": "inline-block"}

    elif level == 'time':
        grouped = defaultdict(int)
        for row in data:
            if row['customer'] == customer and row['product'] == product:
                grouped[row['date'].date()] += row['quantity']
        dates = sorted(grouped.keys())
        values = [grouped[d] for d in dates]
        fig = go.Figure(data=[
            go.Bar(x=dates, y=values, textposition='auto')
        ])
        fig.update_layout(title=f"{product} purchases by {customer} over time")
        back_style = {"display": "inline-block"}

    return fig, back_style

# Update drilldown state
@app.callback(
    Output('current-level', 'data'),
    Output('selected-customer', 'data'),
    Output('selected-product', 'data'),
    Input('main-chart', 'clickData'),
    Input('back-button', 'n_clicks'),
    State('current-level', 'data'),
    State('selected-customer', 'data'),
    State('selected-product', 'data')
)
def update_state(clickData, back_clicks, level, customer, product):
    ctx = dash.callback_context
    triggered = ctx.triggered[0]['prop_id']

    if triggered == "main-chart.clickData":
        if level == 'customer':
            return 'product', clickData['points'][0]['x'], None
        elif level == 'product':
            return 'time', customer, clickData['points'][0]['x']
    elif triggered == "back-button.n_clicks":
        if level == 'product':
            return 'customer', None, None
        elif level == 'time':
            return 'product', customer, None

    return level, customer, product

@app.callback(
    Output('raw-data-table', 'data'),
    Output('raw-data-table', 'columns'),
    Input('current-level', 'data'),
    Input('selected-customer', 'data'),
    Input('selected-product', 'data')
)
def update_table(level, customer, product):
    filtered_data = []

    for row in data:
        row_copy = row.copy()
        row_copy['date'] = row_copy['date'].strftime('%Y-%m-%d')  # for display
        if level == 'customer':
            filtered_data.append(row_copy)
        elif level == 'product' and row['customer'] == customer:
            filtered_data.append(row_copy)
        elif level == 'time' and row['customer'] == customer and row['product'] == product:
            filtered_data.append(row_copy)

    if not filtered_data:
        return [], []

    columns = [{"name": k, "id": k} for k in filtered_data[0].keys()]
    return filtered_data, columns


# Run app
if __name__ == '__main__':
    app.run(debug=True)
