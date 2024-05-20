
import requests
import datetime
import pandas as pd
import plotly.graph_objs as go

# Function to get all-time historical data from CryptoCompare
def get_all_time_historical_data(symbol, currency):
    try:
        # Initialize empty dictionary to store all-time historical data
        all_time_data = {}
        
        # Make request to CryptoCompare API for each year of data
        current_year = datetime.datetime.now().year
        start_year = 2010 # CryptoCompare data is available from 2010
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

# Function to calculate rolling Sharpe ratio
def calculate_rolling_sharpe_ratio(data, window):
    returns = data['Close'].pct_change().dropna()
    rolling_mean = returns.rolling(window=window).mean()
    rolling_std = returns.rolling(window=window).std()
    sharpe_ratio = rolling_mean / rolling_std * (252 ** 0.5)  # Annualized Sharpe ratio
    return sharpe_ratio

# Get Bitcoin historical data
bitcoin_data_dict = get_all_time_historical_data('BTC', 'USD')

# Convert dictionary to DataFrame
bitcoin_data = pd.DataFrame(list(bitcoin_data_dict.items()), columns=['Date', 'Close'])
bitcoin_data['Date'] = pd.to_datetime(bitcoin_data['Date'])
bitcoin_data.set_index('Date', inplace=True)
bitcoin_data.sort_index(inplace=True)

# Default window length
default_window = 180

# Calculate rolling Sharpe ratio with default window
rolling_sharpe_ratio = calculate_rolling_sharpe_ratio(bitcoin_data, default_window)

# Create Plotly figure
fig = go.Figure()

# Add rolling Sharpe ratio trace
fig.add_trace(go.Scatter(x=rolling_sharpe_ratio.index, y=rolling_sharpe_ratio,
                         mode='lines',
                         name=f'Rolling {default_window // 30}m Sharpe Ratio',
                         line=dict(color='orange', width=2.25)))  # Set line width to 2

# Function to update plot based on window length
def update_figure(window_length):
    rolling_sharpe_ratio = calculate_rolling_sharpe_ratio(bitcoin_data, window_length)
    return [go.Scatter(x=rolling_sharpe_ratio.index, y=rolling_sharpe_ratio,
                       mode='lines', name=f'Rolling {window_length // 30}m Sharpe Ratio',
                       line=dict(color='orange', width=2.25))]  # Set line width to 2

# Define the buttons
buttons = [
    dict(label='3 Months',
         method='update',
         args=[{'y': [calculate_rolling_sharpe_ratio(bitcoin_data, 60).values],
                'name': 'Rolling 3m Sharpe Ratio'}]),
    dict(label='6 Months',
         method='update',
         args=[{'y': [calculate_rolling_sharpe_ratio(bitcoin_data, 180).values],
                'name': 'Rolling 6m Sharpe Ratio'}]),
    dict(label='12 Months',
         method='update',
         args=[{'y': [calculate_rolling_sharpe_ratio(bitcoin_data, 360).values],
                'name': 'Rolling 12m Sharpe Ratio'}])
]

# Update layout with buttons and styling
fig.update_layout(
    title='Rolling Sharpe Ratio',
    title_font=dict(color='white'),
    xaxis_title='Date',
    xaxis_title_font=dict(color='white'),
    yaxis_title='Sharpe Ratio',
    yaxis_title_font=dict(color='white'),
    plot_bgcolor='black',
    paper_bgcolor='black',
    font=dict(color='white'),
    updatemenus=[dict(active=1, buttons=buttons, direction="down", pad={"r": 10, "t": 10})],
    xaxis=dict(showgrid=False),  # Hide vertical grid lines
    yaxis=dict(showgrid=False)   # Hide horizontal grid lines
)

# Show plot
fig.show()
