import requests
import datetime
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from data.get_historical_data import get_historical_data
def rgb_to_plotly_color(rgb):
    return 'rgb({}, {}, {})'.format(rgb[0], rgb[1], rgb[2])

def get_rainbow_plot(symbol, currency):
    # Get Bitcoin historical data
    prices = get_historical_data(symbol, currency)
    
    # Create a DataFrame with a range index
    data_df = pd.DataFrame(prices, columns=['Close', 'High', 'Low', 'Open', 'Volume'])
    data_df['Date'] = pd.to_datetime(data_df.index, utc=True).tz_convert(None)
    data_df.set_index('Date', inplace=True)
        # Filter data for BTC starting from 2012
    if symbol == "BTC":
        start_date = datetime.datetime(2012, 1, 1)
        data_df = data_df[data_df.index >= start_date]
    
    # Create logarithmic regression line
    log_prices = np.log(data_df['Close'])
    coefficients = np.polyfit(range(len(data_df['Close'])), log_prices, 1)
    log_fit = np.poly1d(coefficients)
    
    # Create the bands
    x = np.arange(len(data_df))
    rainbow_bands = {
        "Maximum Bubble Territory": (np.exp(log_fit(x) + 1.5), [255, 0, 0]),
        "Sell!": (np.exp(log_fit(x) + 1), [255, 127, 0]),
        "FOMO intensifies": (np.exp(log_fit(x) + 0.5), [255, 255, 0]),
        "Fair value": (np.exp(log_fit(x)), [0, 255, 0]),
        "Still cheap": (np.exp(log_fit(x) - 0.5), [0, 0, 255]),
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
    
    # Plot the rainbow chart
    fig = go.Figure()

    # Add the bands
    for band_name, (y_values, color) in adjusted_bands.items():
        fig.add_trace(
            go.Scatter(
                x=data_df.index,
                y=y_values,
                mode='lines',
                name=band_name,
                line=dict(color=rgb_to_plotly_color(color), width=1.5),
                fill='none'
            )
        )
    
    # Add the actual prices
    fig.add_trace(
        go.Scatter(
            x=data_df.index,
            y=data_df['Close'],
            mode='lines',
            name=symbol + ' Close',
            line=dict(color='orange', width=2)
        )
    )
    
    # Layout with black background, white text, and customized axes
    fig.update_layout(
        title=symbol + ' Rainbow Chart',
        xaxis_title='Date',
        yaxis_title='Close (USD)',
        yaxis_type='log',
        plot_bgcolor='rgba(17, 17, 17, 1)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color='white'),
        showlegend=True,
        yaxis=dict(showticklabels=True, showgrid=False),
        title_x=0.5
    )

    fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))

    return fig

if __name__ == "__main__":
    # Example usage
    symbol = "BTC"
    currency = "USD"

    fig = get_rainbow(symbol, currency)
    fig.show()
