import plotly.graph_objects as go
from data.get_historical_data import get_historical_data

# Get all-time historical data from CryptoCompare API
symbol = 'BTC'
currency = 'USD'
btc = get_historical_data(symbol, currency)

# Calculate Z-score as a rolling 43-day average
btc['Z-Score'] = (btc['Close'] - btc['Close'].rolling(window=511).mean()) / btc['Close'].rolling(window=511).std()

# Plotting
fig = go.Figure()

# Bitcoin closing prices (log scale)
fig.add_trace(go.Scatter(x=btc.index, y=btc['Close'], mode='lines', name='Bitcoin Price', line=dict(color='orange')))

# Z-score
fig.add_trace(go.Scatter(x=btc.index, y=btc['Z-Score'], mode='lines', name='Z-Score', line=dict(color='deeppink'), yaxis='y2'))

# Add horizontal lines at y = 2 and y = -2 on the Z-score axis with thicker lines
fig.update_layout(
    shapes=[
        dict(
            type="line",
            xref="paper",
            yref="y2",
            x0=0,
            y0=6,
            x1=1,
            y1=6,
            line=dict(color="rgba(255, 0, 0, 0.7)", width=3, dash="dash"),
            layer="below"
        ),
        dict(
            type="line",
            xref="paper",
            yref="y2",
            x0=0,
            y0=-1.35,
            x1=1,
            y1=-1.35,
            line=dict(color="rgba(0, 255, 0, 0.5)", width=3, dash="dash"),
            layer="below"
        )
    ]
)

# Update layout
fig.update_layout(
    title='Z-Score Analysis for Bitcoin Price',
    xaxis=dict(title='Date'),
    yaxis=dict(title='Bitcoin Price (USD)', side='left', type='log', tickfont=dict(color='orange')),  # Set log scale for Bitcoin price axis
    yaxis2=dict(title='Z-Score', overlaying='y', side='right', position=0.85, tickfont=dict(color='white')),
    plot_bgcolor='black',
    paper_bgcolor='black',
    font=dict(color='white'),
    xaxis_showgrid=False,  # Remove x-axis gridlines
    yaxis_showgrid=False,  # Remove y-axis gridlines
    yaxis2_showgrid=False  # Remove y-axis gridlines for Z-score axis
)

# Show plot
fig.show()

    
fig.write_html("z_score_btc.html")
