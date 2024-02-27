import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

# Define function to fetch historical market data from CoinGecko
def get_historical_data(start_date, end_date):
    url = f'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range?vs_currency=usd&from={start_date}&to={end_date}'
    response = requests.get(url)
    data = response.json()
    prices = data['prices']
    dates = [pd.to_datetime(x[0], unit='ms') for x in prices]
    prices = [x[1] for x in prices]
    return pd.DataFrame({'Date': dates, 'Price': prices})

# Calculate Realized Value (Simple Moving Average)
def calculate_realized_value(prices, window=180):
    return prices.rolling(window=window).mean()

# Calculate Unrealized Profit/Loss (UPL)
def calculate_upl(prices, realized_value):
    return prices - realized_value

# Calculate NUPL indicator
def calculate_nupl(upl, prices):
    return (upl / prices) * 100  # Multiply by 100 to represent as percentage

# Calculate Z-score
def calculate_z_score(data):
    return (data - data.mean()) / data.std()

# Define start and end dates for data retrieval
start_date = '1293840000'  # 2011-01-01 in Unix timestamp
end_date = str(int(datetime.now().timestamp()))

# Fetch historical market data for Bitcoin
bitcoin_data = get_historical_data(start_date, end_date)

# Calculate Realized Value (Simple Moving Average)
bitcoin_data['Realized_Value'] = calculate_realized_value(bitcoin_data['Price'])

# Calculate Unrealized Profit/Loss (UPL)
bitcoin_data['UPL'] = calculate_upl(bitcoin_data['Price'], bitcoin_data['Realized_Value'])

# Calculate NUPL indicator
bitcoin_data['NUPL'] = calculate_nupl(bitcoin_data['UPL'], bitcoin_data['Price'])

# Calculate Z-score for NUPL
bitcoin_data['NUPL_Z_Score'] = calculate_z_score(bitcoin_data['NUPL'])

# Create subplots with shared x-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add trace for Z-scored NUPL indicator
fig.add_trace(go.Scatter(x=bitcoin_data['Date'], y=bitcoin_data['NUPL_Z_Score'], mode='lines', name='NUPL (Z-Score)', line=dict(color='white')), secondary_y=False)

# Add trace for Bitcoin price
fig.add_trace(go.Scatter(x=bitcoin_data['Date'], y=bitcoin_data['Price'], mode='lines', name='Bitcoin Price', line=dict(color='orange')), secondary_y=True)

# Add neon green line at -3 on NUPL axis
fig.add_shape(type="line", x0=bitcoin_data['Date'].iloc[0], y0=-3, x1=bitcoin_data['Date'].iloc[-1], y1=-3,
              line=dict(color="lime", width=2, dash='dashdot'), secondary_y=False)

# Add neon red line at 2 on NUPL axis
fig.add_shape(type="line", x0=bitcoin_data['Date'].iloc[0], y0=2, x1=bitcoin_data['Date'].iloc[-1], y1=2,
              line=dict(color="red", width=2, dash='dashdot'), secondary_y=False)

# Update layout
fig.update_layout(
    title_text='Bitcoin Relative Unrealized Profit/Loss (NUPL) Indicator with Price',
    xaxis_title='Date',
    font=dict(family='Arial, sans-serif', color='white'),  # Set text color to white
    plot_bgcolor='black',  # Set background color to black
    paper_bgcolor='black',  # Set paper color to black
    legend=dict(font=dict(color='white')),  # Set legend text color to white
    hovermode='x unified'
)

# Update y-axis properties to remove gridlines
fig.update_yaxes(showgrid=False, secondary_y=False)
fig.update_yaxes(showgrid=False, secondary_y=True)

# Update y-axis properties
fig.update_yaxes(title_text="NUPL (Z-Score)", color='white', secondary_y=False)
fig.update_yaxes(title_text="Bitcoin Price (USD)", color='orange', type='log', secondary_y=True)

fig.show()