
import requests
import datetime
import pandas as pd
import plotly.graph_objs as go
from data.get_historical_data import get_historical_data

# Function to calculate rolling Sharpe ratio
def calculate_rolling_sharpe_ratio(data, window):
    returns = data['Close'].pct_change().dropna()
    rolling_mean = returns.rolling(window=window).mean()
    rolling_std = returns.rolling(window=window).std()
    sharpe_ratio = rolling_mean / rolling_std * (252 ** 0.5)  # Annualized Sharpe ratio
    return sharpe_ratio
    
def get_sharpe(symbol,currency):
    # Get crypto historical data
    crypto_data_dict = get_all_time_historical_data(symbol, currency)
    
    # Convert dictionary to DataFrame
    crypto_data = pd.DataFrame(list(crypto_data_dict.items()), columns=['Date', 'Close'])
    crypto_data['Date'] = pd.to_datetime(crypto_data['Date'])
    crypto_data.set_index('Date', inplace=True)
    crypto_data.sort_index(inplace=True)
    
    # Default window length
    default_window = 180
    
    # Calculate rolling Sharpe ratio with default window
    rolling_sharpe_ratio = calculate_rolling_sharpe_ratio(crypto_data, default_window)
    
    # Create Plotly figure
    fig = go.Figure()
    
    # Add rolling Sharpe ratio trace
    fig.add_trace(go.Scatter(x=rolling_sharpe_ratio.index, y=rolling_sharpe_ratio,
                             mode='lines',
                             name=f'Rolling {default_window // 30}m Sharpe Ratio',
                             line=dict(color='orange', width=2.25)))  # Set line width to 2
    
    # Function to update plot based on window length
    def update_figure(window_length):
        rolling_sharpe_ratio = calculate_rolling_sharpe_ratio(crypto_data, window_length)
        return [go.Scatter(x=rolling_sharpe_ratio.index, y=rolling_sharpe_ratio,
                           mode='lines', name=f'Rolling {window_length // 30}m Sharpe Ratio',
                           line=dict(color='orange', width=2.25))]  # Set line width to 2
    
    # Define the buttons
    buttons = [
        dict(label='3 Months',
             method='update',
             args=[{'y': [calculate_rolling_sharpe_ratio(crypto_data, 60).values],
                    'name': 'Rolling 3m Sharpe Ratio'}]),
        dict(label='6 Months',
             method='update',
             args=[{'y': [calculate_rolling_sharpe_ratio(crypto_data, 180).values],
                    'name': 'Rolling 6m Sharpe Ratio'}]),
        dict(label='12 Months',
             method='update',
             args=[{'y': [calculate_rolling_sharpe_ratio(crypto_data, 360).values],
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

return fig

if __name__ == "__main__":
    # Get all-time historical data from CryptoCompare API
    symbol = "BTC"
    currency = "USD"

    fig = get_sharpe(symbol, currency)

    fig.show()
