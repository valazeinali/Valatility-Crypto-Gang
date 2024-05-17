import numpy as np
import plotly.graph_objs as go

from data.get_historical_data import (  # feel free to comment this back in and comment the one below out
    get_coinmetrics_data,
    get_historical_data,
)


def get_s2f_plot(symbol, currency):
    # function to calculate fair-value of bitcoin using S2F model
    def calculate_expression(SF):
        result = np.exp(-1.84) * (SF**3.36)
        return result

    data = get_coinmetrics_data(symbol)

    data["lnMC"] = np.log(data["CapMrktCurUSD"])
    data["lndiff"] = np.log(data["DiffMean"])
    data["issuance_avg"] = data["issuance"].resample("W").mean(numeric_only=True)
    data["fwd_issuance"] = data["issuance"] * 365
    data["s2f"] = data["tsupply"] / data["fwd_issuance"]
    data["lns2f"] = np.log(data["s2f"])
    data = data.resample("W").mean(numeric_only=True)

    # apply function to s2f to get BTC fair-value
    data["Model BTC Price"] = calculate_expression(data["s2f"])

    # Get all-time historical data from CryptoCompare API
    hdata = get_historical_data(symbol, currency)
    # Create an interactive plotly graph
    fig = go.Figure()

    # Add Bitcoin closing prices
    fig.add_trace(
        go.Scatter(
            x=hdata.index,
            y=hdata["Close"],
            mode="lines",
            name=symbol + " Close Price",
            line=dict(color="orange"),
        )
    )

    # Add s2f model
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Model " + symbol + " Price"],
            mode="lines",
            name="s2f model",
            line=dict(color="CYAN"),
        )
    )

    # Set layout with black background
    fig.update_layout(
        title=symbol + "$ 1D vs Stock-to-Flow Modeled Price",
        title_x=0.5,
        xaxis=dict(title="Date"),
        plot_bgcolor="rgba(17, 17, 17, 1)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font=dict(color="white"),
        yaxis=dict(showticklabels=True, showgrid=False, title="Price", type="log")
    )

    fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))

    return fig


if __name__ == "__main__":
    # Get all-time historical data from CryptoCompare API
    symbol = "BTC"
    currency = "USD"

    fig = get_s2f_plot(symbol, currency)

    fig.show()
