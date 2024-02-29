import numpy as np
import plotly.graph_objs as go

from data.get_historical_data import get_historical_data


def get_pi_top_plot(symbol, currency):
    data = get_historical_data(symbol, currency)

    # Calculate moving averages
    data["111DMA"] = data["Close"].rolling(window=111).mean()
    data["350DMA*2"] = data["Close"].rolling(window=350).mean() * 2

    # Calculate Pi Cycle Top Indicator
    data["PiTop"] = data[["111DMA", "350DMA*2"]].max(axis=1)

    # Find where 111DMA > 350DMA * 2
    data["Highlight"] = data["111DMA"] > data["350DMA*2"]

    # Create an interactive plotly graph
    fig = go.Figure()

    # Add Bitcoin closing prices
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Close"],
            mode="lines",
            name=symbol + " Close Price",
            line=dict(color="orange"),
        )
    )

    # Add moving averages
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["111DMA"],
            mode="lines",
            name="111-day Moving Average",
            line=dict(color="#FF97FF"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["350DMA*2"],
            mode="lines",
            name="350-day Moving Average x2",
            line=dict(color="CYAN"),
        )
    )

    # Add Pi Cycle Top Indicator
    # fig.add_trace(go.Scatter(x=data.index, y=data['PiTop'], mode='lines', name='Pi Cycle Top Indicator', line=dict(color='red')))

    # Highlight areas where 111DMA > 350DMA * 2
    highlighted_dates = data[data["Highlight"]].index
    highlighted_prices = data[data["Highlight"]]["Close"]
    fig.add_trace(
        go.Scatter(
            x=highlighted_dates,
            y=highlighted_prices,
            mode="markers",
            marker=dict(color="red", size=6),
            name="111DMA > (350DMA * 2)",
        )
    )

    # Set layout with black background
    fig.update_layout(
        title=symbol + "$ 1D with Moving Averages and Pi Cycle Top Indicator",
        title_x=0.5,
        xaxis=dict(title="Date"),
        yaxis=dict(title="Price", type="log"),
        plot_bgcolor="rgba(17, 17, 17, 1)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font=dict(color="white"),
    )

    fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))

    return fig


if __name__ == "__main__":
    # Get all-time historical data from CryptoCompare API
    symbol = "BTC"
    currency = "USD"

    fig = get_pi_top_plot(symbol, currency)

    fig.show()
