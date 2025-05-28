#import webbrowser
from DashApp import create_app
import datetime

data1 = [
    {"date": datetime.datetime(2025, 4, 1), "customer": "Alice", "product": "Apples", "quantity": 2, "price": 3.5},
    {"date": datetime.datetime(2025, 4, 2), "customer": "Alice", "product": "Bananas", "quantity": 3, "price": 2.0},
    {"date": datetime.datetime(2025, 4, 1), "customer": "Bob", "product": "Apples", "quantity": 5, "price": 3.8},
    # ... и другие строки ...
]
data = [
    {"date": datetime.datetime(2025, 4, 3), "customer": "Alice", "product": "Oranges", "quantity": 4, "price": 2.5},
    {"date": datetime.datetime(2025, 4, 4), "customer": "Alice", "product": "Bananas", "quantity": 2, "price": 2.2},
    {"date": datetime.datetime(2025, 4, 8), "customer": "Alice", "product": "Cars", "quantity": 2, "price": 2.2},
    {"date": datetime.datetime(2025, 4, 9), "customer": "Alice", "product": "Oranges", "quantity": 2, "price": 2.5},
    {"date": datetime.datetime(2025, 4, 3), "customer": "Bob", "product": "Cars", "quantity": 1, "price": 30000},
    {"date": datetime.datetime(2025, 4, 4), "customer": "Bob", "product": "Apples", "quantity": 5, "price": 3.8},
    {"date": datetime.datetime(2025, 4, 5), "customer": "Charlie", "product": "Bikes", "quantity": 2, "price": 450},
    {"date": datetime.datetime(2025, 4, 6), "customer": "Charlie", "product": "Apples", "quantity": 3, "price": 3.6},
]

app = create_app(data)

if __name__ == "__main__":
    #webbrowser.open("http://127.0.0.1:8050")
    try:
        app.run(port=8081, debug=True, use_reloader=True)  # Use reloader=False to avoid issues with reloading
    except KeyboardInterrupt:
        print("Server stopped by KeyboardInterrupt")
        exit()
    #app.run(debug=True)