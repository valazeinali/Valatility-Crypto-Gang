import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from data.get_historical_data import get_historical_data


# Calculate Realized Value (Simple Moving Average)
def calculate_realized_value(Closes, window=180):
    return Closes.rolling(window=window).mean()


# Calculate Unrealized Profit/Loss (UPL)
def calculate_upl(Closes, realized_value):
    return Closes - realized_value


# Calculate NUPL indicator
def calculate_nupl(upl, Closes):
    return (upl / Closes) * 100  # Multiply by 100 to represent as percentage


# Calculate Z-score
def calculate_z_score(data):
    return (data - data.mean()) / data.std()


def get_nupl_score_plot(symbol, currency):
    # Fetch historical market data for Bitcoin
    data = get_historical_data(symbol, currency)

    # Calculate Realized Value (Simple Moving Average)
    data["Realized_Value"] = calculate_realized_value(data["Close"])

    # Calculate Unrealized Profit/Loss (UPL)
    data["UPL"] = calculate_upl(data["Close"], data["Realized_Value"])

    # Calculate NUPL indicator
    data["NUPL"] = calculate_nupl(data["UPL"], data["Close"])

    # Calculate Z-score for NUPL
    data["NUPL_Z_Score"] = calculate_z_score(data["NUPL"])

    # Create subplots with shared x-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add trace for Z-scored NUPL indicator
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["NUPL_Z_Score"],
            mode="lines",
            name="NUPL (Z-Score)",
            line=dict(color="white"),
        ),
        secondary_y=False,
    )

    # Add trace for Bitcoin Close
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Close"],
            mode="lines",
            name=symbol + "$ 1D Close",
            line=dict(color="orange"),
        ),
        secondary_y=True,
    )

    # Add neon green line at -2 on NUPL axis
    fig.add_shape(
        type="line",
        x0=data.index[0],
        y0=-2,
        x1=data.index[-1],
        y1=-2,
        line=dict(color="lime", width=2, dash="dashdot"),
        secondary_y=False,
    )

    # Add neon red line at 2 on NUPL axis
    fig.add_shape(
        type="line",
        x0=data.index[0],
        y0=2,
        x1=data.index[-1],
        y1=2,
        line=dict(color="red", width=2, dash="dashdot"),
        secondary_y=False,
    )

    # Update layout
    fig.update_layout(
        title_text=symbol
        + "$ 1D Relative Unrealized Profit/Loss (NUPL) Indicator with Close",
        title_x=0.5,
        xaxis_title="Date",
        font=dict(family="Arial, sans-serif", color="white"),  # Set text color to white
        plot_bgcolor="rgba(17, 17, 17, 1)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        legend=dict(font=dict(color="black")),  # Set legend text color to white
        hovermode="x unified",
    )

    fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))

    # Update y-axis properties to remove gridlines
    fig.update_yaxes(showgrid=False, secondary_y=False)
    fig.update_yaxes(showgrid=False, secondary_y=True)

    # Update y-axis properties
    fig.update_yaxes(title_text="NUPL (Z-Score)", color="white", secondary_y=False)
    fig.update_yaxes(
        title_text=symbol + "$ 1D Close", color="orange", type="log", secondary_y=True
    )

    return fig


if __name__ == "__main__":
    # Get all-time historical data from CryptoCompare API
    symbol = "BTC"
    currency = "USD"

    fig = get_nupl_score(symbol, currency)

    fig.show()
