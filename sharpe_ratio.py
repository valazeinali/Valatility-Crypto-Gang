import requests
import datetime
import pandas as pd
import plotly.graph_objects as go
from data.get_historical_data import get_historical_data

# Function to calculate rolling Sharpe ratio
def calculate_rolling_sharpe_ratio(data, window):
    returns = data['Close'].pct_change().dropna()
    rolling_mean = returns.rolling(window=window).mean()
    rolling_std = returns.rolling(window=window).std()
    sharpe_ratio = rolling_mean / rolling_std * (252 ** 0.5)  # Annualized Sharpe ratio
    return sharpe_ratio

def get_sharpe_plot(symbol, currency):
    # Get crypto historical data
    crypto_data = get_historical_data(symbol, currency)
    
    # Create a DataFrame with the Date as the index
    data_df = pd.DataFrame(crypto_data, columns=['Close'])
    data_df['Date'] = pd.to_datetime(data_df.index, utc=True).tz_convert(None)
    data_df.set_index('Date', inplace=True)
    
    # Default window length
    default_window = 180
    
    # Calculate rolling Sharpe ratio with default window
    rolling_sharpe_ratio = calculate_rolling_sharpe_ratio(data_df, default_window)
    
    # Create Plotly figure
    fig = go.Figure()
    
    # Add rolling Sharpe ratio trace
    fig.add_trace(go.Scatter(x=rolling_sharpe_ratio.index, y=rolling_sharpe_ratio,
                             mode='lines',
                             name=f'Rolling {default_window // 30}m Sharpe Ratio',
                             line=dict(color='orange', width=2.25)))  # Set line width to 2.25
    
    # Update layout with buttons and aesthetics similar to get_rainbow
    fig.update_layout(
        title=f'{symbol} Rolling Sharpe Ratio',
        xaxis_title='Date',
        yaxis_title='Sharpe Ratio',
        plot_bgcolor='rgba(17, 17, 17, 1)',  # Black background color
        paper_bgcolor='rgba(0, 0, 0, 0)',    # Transparent paper color
        font=dict(color='white'),
        updatemenus=[dict(
            active=1,
            buttons=[
                dict(label='3 Months',
                     method='update',
                     args=[{'y': [calculate_rolling_sharpe_ratio(data_df, 60).values],
                            'name': 'Rolling 3m Sharpe Ratio'}]),
                dict(label='6 Months',
                     method='update',
                     args=[{'y': [calculate_rolling_sharpe_ratio(data_df, 180).values],
                            'name': 'Rolling 6m Sharpe Ratio'}]),
                dict(label='12 Months',
                     method='update',
                     args=[{'y': [calculate_rolling_sharpe_ratio(data_df, 360).values],
                            'name': 'Rolling 12m Sharpe Ratio'}])
            ],
            direction="down",
            pad={"r": 10, "t": 10}
        )],
        xaxis=dict(showgrid=False),  # Hide vertical grid lines
        yaxis=dict(showgrid=False),  # Hide horizontal grid lines
        title_x=0.5
    )

    fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))

    return fig

if __name__ == "__main__":
    # Example usage
    symbol = "ETH"
    currency = "USD"

    fig = get_sharpe_plot(symbol, currency)
    fig.show()
