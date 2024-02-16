import numpy as np
import pandas as pd
from datetime import datetime
import os
from datetime import date
from coinmetrics.api_client import CoinMetricsClient
import warnings
import math
import requests
from datetime import datetime, timedelta
import plotly.graph_objs as go
#from data.get_historical_data import get_historical_data # feel free to comment this back in and comment the one below out
from get_historical_data import get_historical_data

warnings.filterwarnings("ignore")

def get_s2f_plot():
    # function to calculate fair-value of bitcoin using S2F model
    def calculate_expression(SF):
        result = np.exp(-1.84) * (SF ** 3.36)
        return result
        
    def build_s2f(begin_timestamp, end_timestamp):
        client = CoinMetricsClient()
        asset = "btc"
        metrics = "SplyCur,IssContNtv,CapMrktCurUSD,PriceUSD,DiffMean"
        
                # string of format %Y-%m-%d also accepted
        if "datetime" in str(type(begin_timestamp)):
            begin_timestamp = begin_timestamp.strftime("%Y-%m-%d")
        if "datetime" in str(type(end_timestamp)):
            end_timestamp = end_timestamp.strftime("%Y-%m-%d")
        
        asset_data = client.get_asset_metrics(assets=asset, metrics=metrics, start_time=begin_timestamp, end_time=end_timestamp)
    
        raw_data = pd.DataFrame(asset_data)
        mydates = pd.date_range(begin_timestamp, end_timestamp).tolist()
        cleaned_data = pd.DataFrame(index=pd.DatetimeIndex(mydates), data=raw_data.values, columns=raw_data.columns)
    
        cleaned_data.rename(columns={"SplyCur": "tsupply", "IssContNtv": "issuance"}, inplace=True)
        cleaned_data = cleaned_data.astype({'tsupply': 'float', 'issuance': 'float', 'CapMrktCurUSD': 'float', 'DiffMean': 'float'})
    
        cleaned_data['lnMC'] = np.log(cleaned_data['CapMrktCurUSD'])
        cleaned_data['lndiff'] = np.log(cleaned_data['DiffMean'])
        cleaned_data['issuance_avg'] = cleaned_data['issuance'].resample('W').mean(numeric_only=True)
        cleaned_data['fwd_issuance'] = cleaned_data['issuance'] * 365
        cleaned_data['s2f'] = cleaned_data['tsupply'] / cleaned_data['fwd_issuance']
        cleaned_data['lns2f'] = np.log(cleaned_data['s2f'])
        cleaned_data = cleaned_data.resample('W').mean(numeric_only=True)
    
        return cleaned_data
    
    # Get today's date
    today = datetime.now().date()
    
    # Calculate yesterday's date
    yesterday = today - timedelta(days=1)
    
    # Save yesterday's date as end_date
    end_date = yesterday
    
    start='2010-01-01'
    end = end_date
    df = build_s2f(start, end)
    
    # apply function to s2f to get BTC fair-value
    df["Model BTC Price"] = calculate_expression(df["s2f"])
    
    # Get all-time historical data from CryptoCompare API
    symbol = 'BTC'
    currency = 'USD'
    btc = get_historical_data(symbol, currency)

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
        plot_bgcolor='#111111',
        paper_bgcolor='#111111',
        font=dict(color='white')
    )
    fig.show()
    fig.write_html("vala_s2f_model.html")
    return fig

get_s2f_plot()