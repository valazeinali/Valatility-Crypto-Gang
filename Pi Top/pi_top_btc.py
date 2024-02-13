import yfinance as yf
import plotly.graph_objs as go

# Retrieve Bitcoin daily prices
btc = yf.download('BTC-USD', start='2010-01-01', end='2100-02-13')

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
    plot_bgcolor='black',
    paper_bgcolor='black',
    font=dict(color='white')
)

# Show the graph
fig.show()

fig.write_html("pi_top_btc.html")