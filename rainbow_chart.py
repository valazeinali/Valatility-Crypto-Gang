import requests
import datetime
import numpy as np
import pandas as pd
import plotly.graph_objects as go

def get_all_time_historical_data(symbol, currency):
    try:
        # Initialize empty dictionary to store all-time historical data
        all_time_data = {}
        
        # Make request to CryptoCompare API for each year of data
        current_year = datetime.datetime.now().year
        start_year = 2012 # CryptoCompare data is available from 2010
        for year in range(start_year, current_year + 1):
            end_date = datetime.datetime(year + 1, 1, 1)
            start_date = datetime.datetime(year, 1, 1)

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
                date = datetime.datetime.utcfromtimestamp(entry['time']).strftime('%Y-%m-%d')
                all_time_data[date] = entry['close']

        return all_time_data
    except Exception as e:
        print("An error occurred:", e)
        return None

# Get Bitcoin historical data
bitcoin_data = get_all_time_historical_data('BTC', 'USD')

# Convert data to DataFrame
bitcoin_df = pd.DataFrame(list(bitcoin_data.items()), columns=['Date', 'Price'])
bitcoin_df['Date'] = pd.to_datetime(bitcoin_df['Date'])
bitcoin_df.set_index('Date', inplace=True)

# Filter out zero or negative prices
positive_prices = bitcoin_df[bitcoin_df['Price'] > 0]['Price']

# Create logarithmic regression line
log_prices = np.log(positive_prices)
coefficients = np.polyfit(range(len(positive_prices)), log_prices, 1)
log_fit = np.poly1d(coefficients)

def rgb_to_plotly_color(rgb):
    return 'rgb({}, {}, {})'.format(rgb[0], rgb[1], rgb[2])

# Create the bands
x = np.arange(len(bitcoin_df))
rainbow_bands = {
    "Maximum Bubble Territory": (np.exp(log_fit(x) + 1.5), [255, 0, 0]),
    "Sell!": (np.exp(log_fit(x) + 1), [255, 127, 0]),
    "FOMO intensifies": (np.exp(log_fit(x) + 0.5), [255, 255, 0]),
    "Fair value": (np.exp(log_fit(x)), [0, 255, 0]),
    "Still cheap": (np.exp(log_fit(x) - 0.5), [0,0,255]),
    "Accumulate": (np.exp(log_fit(x) - 1), [75, 0, 130]),
    "Buy!": (np.exp(log_fit(x) - 1.5), [143, 0, 255])
}

# Adjust bands so they don't stack
adjusted_bands = {}
prev_y_values = None
for band_name, (y_values, color) in rainbow_bands.items():
    if prev_y_values is None:
        adjusted_bands[band_name] = (y_values, color)
    else:
        # Adjust the starting point of y-values to prevent stacking
        adjusted_y_values = y_values / prev_y_values.max() * prev_y_values[-1]
        adjusted_bands[band_name] = (adjusted_y_values, color)
    prev_y_values = adjusted_bands[band_name][0]
    
# Plot
fig = go.Figure()

# Add the bands
for band_name, (y_values, color) in adjusted_bands.items():
    fig.add_trace(go.Scatter(
        x=bitcoin_df.index,
        y=y_values,
        mode='lines',
        name=band_name,
        line=dict(color=rgb_to_plotly_color(color), width=1.5),
        fill='none'
    ))

# Add the actual prices
fig.add_trace(go.Scatter(
    x=bitcoin_df.index,
    y=bitcoin_df['Price'],
    mode='lines',
    name='Bitcoin Price',
    line=dict(color='orange', width=2)
))

# Layout with black background, white text, and no y-axis ticks
fig.update_layout(
    title="Bitcoin Rainbow Chart",
    xaxis_title="Date",
    yaxis_title="Price (USD)",
    yaxis_type="log",
    showlegend=True,
    plot_bgcolor='black',
    paper_bgcolor='black',
    font=dict(color='white'),
    yaxis=dict(showticklabels=True, showgrid=False)
)

fig.show()