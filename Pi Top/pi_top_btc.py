from datetime import datetime, timedelta

import pandas as pd
import plotly.graph_objs as go
import requests
import yfinance as yf

# Retrieve Bitcoin daily prices
# btc = yf.download('BTC-USD', start='2010-01-01', end='2100-02-13')


# get data
def get_all_time_historical_data(symbol, currency):
    try:
        # Initialize empty dictionary to store all-time historical data
        all_time_data = {}

        # Make request to CryptoCompare API for each year of data
        current_year = datetime.now().year
        start_year = 2010  # CryptoCompare data is available from 2010
        for year in range(start_year, current_year + 1):
            end_date = datetime(year + 1, 1, 1)
            start_date = datetime(year, 1, 1)

            # Convert dates to Unix timestamp format
            end_date_unix = int(end_date.timestamp())
            start_date_unix = int(start_date.timestamp())

            # Make request to CryptoCompare API
            url = "https://min-api.cryptocompare.com/data/v2/histoday"
            parameters = {
                "fsym": symbol,
                "tsym": currency,
                "limit": (end_date - start_date).days,
                "toTs": end_date_unix,
            }
            response = requests.get(url, params=parameters)
            data = response.json()

            # Extract daily close prices
            for entry in data["Data"]["Data"]:
                date = datetime.utcfromtimestamp(entry["time"]).strftime("%Y-%m-%d")
                all_time_data[date] = entry["close"]

        return all_time_data
    except Exception as e:
        print("An error occurred:", e)
        return None


# Get all-time historical data from CryptoCompare API
symbol = "BTC"
currency = "USD"
bitcoin_all_time_data = get_all_time_historical_data(symbol, currency)

if bitcoin_all_time_data:
    # Create DataFrame from the dictionary
    btc = pd.DataFrame(list(bitcoin_all_time_data.items()), columns=["Date", "Close"])
    btc["Date"] = pd.to_datetime(btc["Date"])  # Convert Date column to datetime type
    btc = btc.set_index("Date")  # Set Date column as index

else:
    print("Failed to retrieve data.")

# Calculate moving averages
btc["111DMA"] = btc["Close"].rolling(window=111).mean()
btc["350DMA*2"] = btc["Close"].rolling(window=350).mean() * 2

# Calculate Pi Cycle Top Indicator
btc["PiTop"] = btc[["111DMA", "350DMA*2"]].max(axis=1)

# Find where 111DMA > 350DMA * 2
btc["Highlight"] = btc["111DMA"] > btc["350DMA*2"]

# Create an interactive plotly graph
fig = go.Figure()

# Add Bitcoin closing prices
fig.add_trace(
    go.Scatter(
        x=btc.index,
        y=btc["Close"],
        mode="lines",
        name="Bitcoin Close Price",
        line=dict(color="orange"),
    )
)

# Add moving averages
fig.add_trace(
    go.Scatter(
        x=btc.index,
        y=btc["111DMA"],
        mode="lines",
        name="111-day Moving Average",
        line=dict(color="#FF97FF"),
    )
)
fig.add_trace(
    go.Scatter(
        x=btc.index,
        y=btc["350DMA*2"],
        mode="lines",
        name="350-day Moving Average x2",
        line=dict(color="CYAN"),
    )
)

# Add Pi Cycle Top Indicator
# fig.add_trace(go.Scatter(x=btc.index, y=btc['PiTop'], mode='lines', name='Pi Cycle Top Indicator', line=dict(color='red')))

# Highlight areas where 111DMA > 350DMA * 2
highlighted_dates = btc[btc["Highlight"]].index
highlighted_prices = btc[btc["Highlight"]]["Close"]
fig.add_trace(
    go.Scatter(
        x=highlighted_dates,
        y=highlighted_prices,
        mode="markers",
        marker=dict(color="red", size=6),
        name="111DMA > (350DMA * 2)",
    )
)

# Set layout with black background
fig.update_layout(
    title="Bitcoin Daily Prices with Moving Averages and Pi Cycle Top Indicator",
    xaxis=dict(title="Date"),
    yaxis=dict(title="Price", type="log"),
    plot_bgcolor="black",
    paper_bgcolor="black",
    font=dict(color="white"),
)

# Show the graph
fig.show()

fig.write_html("pi_top_btc.html")
