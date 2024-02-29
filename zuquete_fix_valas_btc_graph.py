from datetime import datetime

import numpy as np
import pandas as pd
import plotly.graph_objs as go
import requests
import yfinance as yf


def get_all_time_historical_data(symbol, currency):
    try:
        # Initialize empty dictionary to store all-time historical data
        all_time_data = {}

        # Make request to CryptoCompare API for each year of data
        current_year = datetime.now().year
        start_year = 2010  # CryptoCompare data is available from 2010
        for year in range(start_year, current_year):
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


# Get Bitcoin historical data
bitcoin_data = get_all_time_historical_data("BTC", "USD")

# Convert data to DataFrame
bitcoin_df = pd.DataFrame(list(bitcoin_data.items()), columns=["Date", "Price"])
bitcoin_df["Date"] = pd.to_datetime(bitcoin_df["Date"])

# Calculate daily percentage change
bitcoin_df["Percentage Change"] = bitcoin_df["Price"].pct_change()

# Group data by year
bitcoin_df["Year"] = bitcoin_df["Date"].dt.year

# Filter data for years from 2010 to the previous year
current_year = datetime.now().year
bitcoin_df = bitcoin_df[bitcoin_df["Year"] < current_year]

# Calculate cumulative sum of percentage change for each year
yearly_cumulative_percentage_change = bitcoin_df.groupby("Year")[
    "Percentage Change"
].cumsum()

# Calculate median cumulative percentage change for each day of the year
median_cumulative_percentage_change = yearly_cumulative_percentage_change.groupby(
    bitcoin_df["Date"].dt.dayofyear
).median()

# Remove the 366th day if present
if 366 in median_cumulative_percentage_change.index:
    median_cumulative_percentage_change = median_cumulative_percentage_change.drop(
        index=366
    )

# Get today's date
today = datetime.now().date()
# Get the current year
current_year = datetime.now().year

# Define the start date as the beginning of the current year
start_date = f"{current_year}-01-01"

# Fetch historical data for Bitcoin from the start of the current year until the current date
bitcoin = yf.Ticker("BTC-USD")
bitcoin_history = bitcoin.history(
    start=start_date, end=datetime.now().strftime("%Y-%m-%d")
)

# Calculate year-to-date return
year_start_price = bitcoin_history.iloc[0]["Close"]
current_price = bitcoin_history.iloc[-1]["Close"]
btc_ytd_return = ((current_price / year_start_price) - 1) * 100
print(btc_ytd_return)
# Plot the median cumulative percentage change and add a horizontal line for YTD return
fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=median_cumulative_percentage_change.index,
        y=median_cumulative_percentage_change.values * 100,
        mode="lines",
        name="Median Cumulative Percentage Change",
        line=dict(color="orange", width=2),
    )
)
# Add vertical line for today's date

fig.add_shape(
    type="line",
    x0=today.timetuple().tm_yday,
    y0=-10,
    x1=today.timetuple().tm_yday,
    y1=130,
    line=dict(color="white", width=1.5, dash="dash"),
)
# Add horizontal line for YTD return

fig.add_shape(
    type="line",
    x0=median_cumulative_percentage_change.index.min(),
    y0=btc_ytd_return,
    x1=median_cumulative_percentage_change.index.max(),
    y1=btc_ytd_return,
    line=dict(color="white", width=1.5, dash="dash"),
)

fig.update_layout(
    title="Median Cumulative Percentage Change of Bitcoin (2010 to Previous Year)",
    xaxis_title="Day of the Year",
    yaxis_title="Median Cumulative Percentage Change",
    plot_bgcolor="black",
    paper_bgcolor="black",  # Set overall background color of the chart
    font=dict(color="white"),
    showlegend=True,
    width=1000,  # Adjust width
    height=600,
)  # Adjust height

fig.show()
