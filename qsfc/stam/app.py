import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from datetime import datetime
from collections import defaultdict

# Sample Data
data = [
    {'date': '2025-04-01', 'customer': 'Alice', 'total': 120, 'product': 'Apples', 'quantity': 2},
    {'date': '2025-04-02', 'customer': 'Alice', 'total': 140, 'product': 'Cars', 'quantity': 3},
    {'date': '2025-04-01', 'customer': 'Bob', 'total': 90, 'product': 'Cars', 'quantity': 4},
    {'date': '2025-04-02', 'customer': 'Bob', 'total': 130, 'product': 'Apples', 'quantity': 5},
    {'date': '2025-04-03', 'customer': 'Alice', 'total': 100, 'product': 'Apples', 'quantity': 6},
    {'date': '2025-04-03', 'customer': 'Bob', 'total': 60, 'product': 'Apples', 'quantity': 2},
    {'date': '2025-04-03', 'customer': 'Alice', 'total': 100, 'product': 'Apples', 'quantity': 6},
]

# Convert date strings to datetime objects
for row in data:
    row['date'] = datetime.strptime(row['date'], "%Y-%m-%d")

# Initialize app
app = dash.Dash(__name__)
server = app.server  # for deployment

# Get list of unique customers
customers = sorted(set(row['customer'] for row in data))

# App layout
app.layout = html.Div([
    html.H2("📊 Dashboard: Totals by Customer and Date"),

    html.Label("Select Customer(s):"),
    dcc.Dropdown(
        id='customer-dropdown',
        options=[{'label': c, 'value': c} for c in customers],
        value=customers,  # Default: all selected
        multi=True
    ),

    html.Br(),

    html.Label("Select Date Range:"),
    dcc.DatePickerRange(
        id='date-picker',
        min_date_allowed=min(row['date'] for row in data),
        max_date_allowed=max(row['date'] for row in data),
        start_date=min(row['date'] for row in data),
        end_date=max(row['date'] for row in data)
    ),

    html.Br(), html.Br(),

    dcc.Graph(id='bar-chart')
])

# Callback to update graph
@app.callback(
    Output('bar-chart', 'figure'),
    Input('customer-dropdown', 'value'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date')
)
def update_chart(selected_customers, start_date, end_date):
    start = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)

    # Filter data
    filtered = [row for row in data if row['customer'] in selected_customers and start <= row['date'] <= end]

    # Group by customer and date
    grouped = defaultdict(lambda: defaultdict(float))
    for row in filtered:
        grouped[row['customer']][row['date'].date()] += row['total']

    all_dates = sorted(set(row['date'].date() for row in filtered))
    fig = go.Figure()

    for customer in selected_customers:
        y_values = [grouped[customer].get(date, 0) for date in all_dates]
        fig.add_trace(go.Bar(
            name=customer,
            x=all_dates,
            y=y_values,
            text=[f"{customer}: {v}" for v in y_values],
            textposition='auto'
        ))

    fig.update_layout(
        title="Сумма по датам и клиентам",
        xaxis_title="Дата",
        yaxis_title="Сумма",
        barmode='group',
        width=1000
    )
    return fig

# Run server
if __name__ == '__main__':
    app.run(debug=True)
