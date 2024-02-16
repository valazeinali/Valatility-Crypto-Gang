import requests
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import pandas as pd

# Retrieve Bitcoin daily prices
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
            url = 'https://min-api.cryptocompare.com/data/v2/histoday'
            parameters = {
                'fsym': symbol,
                'tsym': currency,
                'limit': (end_date - start_date).days,
                'toTs': end_date_unix
            }
            response = requests.get(url, params=parameters)
            data = response.json()

            # Extract daily close prices
            for entry in data['Data']['Data']:
                date = datetime.utcfromtimestamp(entry['time']).strftime('%Y-%m-%d')
                all_time_data[date] = entry['close']

        return all_time_data
    except Exception as e:
        print("An error occurred:", e)
        return None

# Get all-time historical data from CryptoCompare API
symbol = 'BTC'
currency = 'USD'
bitcoin_all_time_data = get_all_time_historical_data(symbol, currency)

if bitcoin_all_time_data:
    # Create DataFrame from the dictionary
    btc = pd.DataFrame(list(bitcoin_all_time_data.items()), columns=['Date', 'Close'])
    btc['Date'] = pd.to_datetime(btc['Date'])  # Convert Date column to datetime type
    btc = btc.set_index('Date')  # Set Date column as index
    
    # Calculate Z-score as a rolling 43-day average
    btc['Z-Score'] = (btc['Close'] - btc['Close'].rolling(window=511).mean()) / btc['Close'].rolling(window=511).std()

    # Plotting
    fig = go.Figure()

    # Bitcoin closing prices (log scale)
    fig.add_trace(go.Scatter(x=btc.index, y=btc['Close'], mode='lines', name='Bitcoin Price', line=dict(color='orange')))

    # Z-score
    fig.add_trace(go.Scatter(x=btc.index, y=btc['Z-Score'], mode='lines', name='Z-Score', line=dict(color='deeppink'), yaxis='y2'))

    # Add horizontal lines at y = 2 and y = -2 on the Z-score axis with thicker lines
    fig.update_layout(
        shapes=[
            dict(
                type="line",
                xref="paper",
                yref="y2",
                x0=0,
                y0=6,
                x1=1,
                y1=6,
                line=dict(color="rgba(255, 0, 0, 0.7)", width=3, dash="dash"),
                layer="below"
            ),
            dict(
                type="line",
                xref="paper",
                yref="y2",
                x0=0,
                y0=-1.35,
                x1=1,
                y1=-1.35,
                line=dict(color="rgba(0, 255, 0, 0.5)", width=3, dash="dash"),
                layer="below"
            )
        ]
    )
    
    # Update layout
    fig.update_layout(
        title='Z-Score Analysis for Bitcoin Price',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Bitcoin Price (USD)', side='left', type='log', tickfont=dict(color='orange')),  # Set log scale for Bitcoin price axis
        yaxis2=dict(title='Z-Score', overlaying='y', side='right', position=0.85, tickfont=dict(color='white')),
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='white'),
        xaxis_showgrid=False,  # Remove x-axis gridlines
        yaxis_showgrid=False,  # Remove y-axis gridlines
        yaxis2_showgrid=False  # Remove y-axis gridlines for Z-score axis
    )

    # Show plot
    fig.show()
else:
    print("Failed to retrieve data.")
    
fig.write_html("z_score_btc.html")