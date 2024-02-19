import plotly.graph_objs as go
from data.get_historical_data import get_historical_data, get_coinmetrics_data # feel free to comment this back in and comment the one below out
import numpy as np

def get_s2f_plot():
    # function to calculate fair-value of bitcoin using S2F model
    def calculate_expression(SF):
        result = np.exp(-1.84) * (SF ** 3.36)
        return result
        
    
    asset = "BTC"
    data = get_coinmetrics_data(asset)
    
    data['lnMC'] = np.log(data['CapMrktCurUSD'])
    data['lndiff'] = np.log(data['DiffMean'])
    data['issuance_avg'] = data['issuance'].resample('W').mean(numeric_only=True)
    data['fwd_issuance'] = data['issuance'] * 365
    data['s2f'] = data['tsupply'] / data['fwd_issuance']
    data['lns2f'] = np.log(data['s2f'])
    data = data.resample('W').mean(numeric_only=True)
    
    

    # apply function to s2f to get BTC fair-value
    data["Model BTC Price"] = calculate_expression(data["s2f"])
    
    # Get all-time historical data from CryptoCompare API
    symbol = 'BTC'
    currency = 'USD'
    btc = get_historical_data(symbol, currency)

    # Create an interactive plotly graph
    fig = go.Figure()
    
    # Add Bitcoin closing prices
    fig.add_trace(go.Scatter(x=btc.index, y=btc['Close'], mode='lines', name='Bitcoin Close Price',line=dict(color='orange')))
    
    # Add s2f model
    fig.add_trace(go.Scatter(x=data.index, y=data['Model BTC Price'], mode='lines', name='s2f model', line=dict(color='CYAN')))
    
    # Set layout with black background
    fig.update_layout(
        title='Bitcoin Daily Prices vs Stock-to-Flow Modeled Price',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Price',type='log'),
        plot_bgcolor='#111111',
        paper_bgcolor='#111111',
        font=dict(color='white')
    )

    fig.write_html("vala_s2f_model.html")
    fig.show()
    return fig

get_s2f_plot()
