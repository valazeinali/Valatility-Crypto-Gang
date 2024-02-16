import numpy as np
import pandas as pd
from datetime import datetime
from datetime import date
from coinmetrics.api_client import CoinMetricsClient
import warnings
import math
import requests
from datetime import datetime, timedelta
import plotly.graph_objs as go
warnings.filterwarnings("ignore")

# function to calculate fair-value of bitcoin using S2F model
def calculate_expression(SF):
    result = math.exp(-1.84) * (SF ** 3.36)
    return result

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
    
def build_s2f(begin_timestamp, end_timestamp):
    # construct the Bitcoin Stock-to-Flow Ratio using the CoinMetrics API
    client = CoinMetricsClient()

    # string of format %Y-%m-%d also accepted
    if "datetime" in str(type(begin_timestamp)):
        begin_timestamp = begin_timestamp.strftime("%Y-%m-%d")
    if "datetime" in str(type(end_timestamp)):
        end_timestamp = end_timestamp.strftime("%Y-%m-%d")

    asset = "btc"
    # define the metrics to fetch
    metrics = "SplyCur,IssContNtv,CapMrktCurUSD,PriceUSD,DiffMean"
    # fetch the metrics
    asset_data = client.get_asset_metrics(assets=asset, metrics=metrics, start_time=begin_timestamp, end_time=end_timestamp)
    raw_data = pd.DataFrame(asset_data)
    # export raw data to csv
    #raw_data.to_csv("CM_raw_data.csv", encoding='utf-8')
    
    # do this dumbass bullshit because pandas resampling without datetimeindex blah blah
    mydates = pd.date_range(begin_timestamp, end_timestamp).tolist()
    mydates = pd.to_datetime(mydates, utc=True)
    mydates = pd.DatetimeIndex(mydates)

    # drop unecessary data
    raw_data.drop(['asset', 'time'], axis=1, inplace=True)
    # create new dataframe for export
    cleaned_data = pd.DataFrame(index=mydates, data=raw_data.values, columns=raw_data.columns)
    # rename columns to be more intuitive
    cleaned_data.rename(columns={"SplyCur": "tsupply", "IssContNtv": "issuance"}, inplace=True)
    # make sure all columns are of type float (recent API update was returning str)
    cleaned_data['tsupply'] = cleaned_data['tsupply'].astype(float)
    cleaned_data['issuance'] = cleaned_data['issuance'].astype(float)
    cleaned_data['CapMrktCurUSD'] = cleaned_data['CapMrktCurUSD'].astype(float)
    cleaned_data['DiffMean'] = cleaned_data['DiffMean'].astype(float)

    # add calculated values to the dataframe
    cleaned_data['lnMC'] = np.log(cleaned_data['CapMrktCurUSD'])
    cleaned_data['lndiff'] = np.log(cleaned_data['DiffMean'])
    cleaned_data['issuance_avg'] = cleaned_data['issuance'].resample('W').mean()
    cleaned_data['fwd_issuance'] = np.multiply(cleaned_data['issuance'], 365)
    cleaned_data['s2f'] = np.divide(cleaned_data[['tsupply']], cleaned_data[['fwd_issuance']])
    cleaned_data['lns2f'] = np.log(cleaned_data[['s2f']])
    # resample the data by week 
    cleaned_data = cleaned_data.resample('W').mean()

    return cleaned_data

# Get today's date
today = datetime.now().date()

# Calculate yesterday's date
yesterday = today - timedelta(days=1)

# Save yesterday's date as end_date
end_date = yesterday

start='2010-01-01'
end= end_date
df = build_s2f(start,end)

# apply function to s2f to get BTC fair-value
df["Model BTC Price"] = calculate_expression(df["s2f"])

# Get all-time historical data from CryptoCompare API
symbol = 'BTC'
currency = 'USD'
bitcoin_all_time_data = get_all_time_historical_data(symbol, currency)

if bitcoin_all_time_data:
    # Create DataFrame from the dictionary
    btc = pd.DataFrame(list(bitcoin_all_time_data.items()), columns=['Date', 'Close'])
    btc['Date'] = pd.to_datetime(btc['Date'])  # Convert Date column to datetime type
    btc = btc.set_index('Date')  # Set Date column as index
    
else:
    print("Failed to retrieve data.")
    

# Create an interactive plotly graph
fig = go.Figure()

# Add Bitcoin closing prices
fig.add_trace(go.Scatter(x=btc.index, y=btc['Close'], mode='lines', name='Bitcoin Close Price',line=dict(color='orange')))

# Add s2f model
fig.add_trace(go.Scatter(x=df.index, y=df['Model BTC Price'], mode='lines', name='s2f model', line=dict(color='CYAN')))

# Set layout with black background
fig.update_layout(
    title='Bitcoin Daily Prices vs Stock-to-Flow Modeled Price',
    xaxis=dict(title='Date'),
    yaxis=dict(title='Price',type='log'),
    plot_bgcolor='black',
    paper_bgcolor='black',
    font=dict(color='white')
)

# Show the graph
fig.show()

fig.write_html("vala_s2f_model.html")
