import plotly.graph_objs as go
import pandas as pd
import requests
from datetime import datetime
import yfinance as yf

def get_pi_cycle_top_plot():
    # get data
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
        
    else:
        print("Failed to retrieve data.")
    
    # Calculate moving averages
    btc['111DMA'] = btc['Close'].rolling(window=111).mean()
    btc['350DMA*2'] = btc['Close'].rolling(window=350).mean()*2
    
    # Calculate Pi Cycle Top Indicator
    btc['PiTop'] = btc[['111DMA', '350DMA*2']].max(axis=1)
    
    # Find where 111DMA > 350DMA * 2
    btc['Highlight'] = btc['111DMA'] > btc['350DMA*2']
    
    # Create an interactive plotly graph
    fig = go.Figure()
    
    # Add Bitcoin closing prices
    fig.add_trace(go.Scatter(x=btc.index, y=btc['Close'], mode='lines', name='Bitcoin Close Price',line=dict(color='orange')))
    
    # Add moving averages
    fig.add_trace(go.Scatter(x=btc.index, y=btc['111DMA'], mode='lines', name='111-day Moving Average', line=dict(color='#FF97FF')))
    fig.add_trace(go.Scatter(x=btc.index, y=btc['350DMA*2'], mode='lines', name='350-day Moving Average x2', line=dict(color='CYAN')))
    
    # Add Pi Cycle Top Indicator
    #fig.add_trace(go.Scatter(x=btc.index, y=btc['PiTop'], mode='lines', name='Pi Cycle Top Indicator', line=dict(color='red')))
    
    # Highlight areas where 111DMA > 350DMA * 2
    highlighted_dates = btc[btc['Highlight']].index
    highlighted_prices = btc[btc['Highlight']]['Close']
    fig.add_trace(go.Scatter(x=highlighted_dates, y=highlighted_prices, mode='markers',
                             marker=dict(color='red', size=6), name='111DMA > (350DMA * 2)'))
    
    # Set layout with black background
    fig.update_layout(
        title='Bitcoin Daily Prices with Moving Averages and Pi Cycle Top Indicator',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Price',type='log'),
        plot_bgcolor='#111111',
        paper_bgcolor='#111111',
        font=dict(color='white')
    )
    return fig


def get_bitcoin_seasonality_heatmap_plot():

    # Define a dictionary to map month numbers to names
    month_names = {
        1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr',
        5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug',
        9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
    }
    
    # Retrieve Bitcoin daily prices
    btc = yf.download('BTC-USD', start='2010-01-01', end='2100-02-13')
    
    # Convert the daily prices to monthly returns
    btc_monthly_returns = btc['Adj Close'].resample('M').ffill().pct_change()
    
    # Create a DataFrame that shows year and month for each row
    btc_monthly_returns_df = pd.DataFrame(btc_monthly_returns)
    btc_monthly_returns_df['Year'] = btc_monthly_returns_df.index.year
    btc_monthly_returns_df['Month'] = btc_monthly_returns_df.index.month
    btc_monthly_returns_df['Returns'] = btc_monthly_returns_df['Adj Close']*100
    
    # Pivot the DataFrame to have years as rows, months as columns, and returns as values
    seasonality_df = btc_monthly_returns_df.pivot(index="Year", columns="Month", values="Returns")
    
    # Generate hover text information
    hover_text = []
    for yi, yy in enumerate(seasonality_df.index):
        hover_text.append([])
        for xi, xx in enumerate(seasonality_df.columns):
            hover_text[-1].append(
                f"Year: {yy}<br>Month: {month_names[xx]}<br>Return: {seasonality_df.values[yi][xi]}%"
            )
            
    # Use Plotly to create the heat map
    fig = go.Figure(data=go.Heatmap(
                        
                       z=seasonality_df,
                       x=[month_names[i] for i in seasonality_df.columns],
                       y=seasonality_df.index,
                       text=hover_text,  # Apply hover text
                       hoverinfo="text",  # Display the text on hover
                       hoverongaps = False,
                       colorscale="Cividis",))
    
    # Add annotations
    for y, year in enumerate(seasonality_df.index):
        for m, month in enumerate(seasonality_df.columns):
            value = seasonality_df.iloc[y, m]
            # Only proceed if value is not NaN
            if not pd.isna(value):
                fig.add_annotation(dict(
                    font=dict(color="white"),
                    x=month_names[month],
                    y=year,
                    text=f"{value:.3}%",
                    showarrow=False,
                    xanchor='center',
                    yanchor='middle',
                    ))
                
    fig.update_layout(title='Bitcoin Monthly Returns (%) Heatmap',
                      xaxis_nticks=12,
                      plot_bgcolor='#111111',
                      paper_bgcolor='#111111',
                      font=dict(color='white'))
    return fig


#########################################################################################################################################################################


from dash import Dash, html, dcc

# Initialize the app
app = Dash(__name__, assets_url_path = 'assets')

app.title = "Valatility"

colors = {
    "main-background": "#111111",
    "header-text": "#ff7575",
    "sub-text": "#ffd175",
    "text": "#ff7575",
}

def send_layout():
    return html.Div(style={'backgroundColor': colors['main-background']}, children=[
        html.H1(
            children='Valatility crypto dashboard ',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),
    
    
        html.Div(children=[
            dcc.Graph(id="Pi Cycle Top", style={'width': '100%', 'vertical-align': 'middle'}, figure=get_pi_cycle_top_plot()),
        ]),
        
        html.Div(children=[
            dcc.Graph(id="Bitcoin Seasonality Heatmap", style={'width': '100%', 'vertical-align': 'middle'}, figure=get_bitcoin_seasonality_heatmap_plot()),
        ])
    ])

app.layout = send_layout

# Run the app
if __name__ == '__main__':
    app.run_server(port=1222)
    
