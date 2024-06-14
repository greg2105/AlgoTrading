import os
import requests
import pandas as pd
import datetime as dt
import plotly.graph_objects as go
from config import polygon_api_key

def get_historical_data(ticker, start_date, end_date):
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{start_date.strftime('%Y-%m-%d')}/{end_date.strftime('%Y-%m-%d')}"
    params = {
        "adjusted": "true",
        "sort": "asc",
        "apiKey": polygon_api_key
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()["results"]
        df = pd.DataFrame(data)
        df["t"] = pd.to_datetime(df["t"], unit="ms")
        df = df.set_index("t")
        return df
    else:
        print(f"Error fetching data for {ticker}: {response.status_code} - {response.text}")
        return None

start_date = dt.datetime(2023, 1, 1)
end_date = dt.datetime(2023, 6, 1)
aapl_data = get_historical_data("AAPL", start_date, end_date)

if aapl_data is not None:
    fig = go.Figure(data=[go.Candlestick(x=aapl_data.index,
                                         open=aapl_data['o'],
                                         high=aapl_data['h'],
                                         low=aapl_data['l'],
                                         close=aapl_data['c'])])
    fig.update_layout(title=f"AAPL Stock Prices ({start_date.date()} - {end_date.date()})",
                      xaxis_title="Date",
                      yaxis_title="Price (USD)")
    fig.show()