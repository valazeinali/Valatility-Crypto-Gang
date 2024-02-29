import plotly.graph_objs as go
from data.get_historical_data import (
    get_historical_data,
    get_coinmetrics_data,
)  # feel free to comment this back in and comment the one below out
from datetime import datetime
import pandas as pd


def get_mcpc_plot(symbol, currency):
    # Get historical data
    data = get_historical_data(symbol, currency)

    # Calculate daily percentage change
    data["Percentage Change"] = data["Close"].pct_change()

    # Group data by year
    data["Year"] = data.index.year

    # Filter data for years from 2010 to the previous year
    current_year = datetime.now().year
    full_years_data = data[data["Year"] < current_year]

    # Calculate cumulative sum of percentage change for each year
    yearly_cumulative_percentage_change = full_years_data.groupby("Year")[
        "Percentage Change"
    ].cumsum()

    # Calculate median cumulative percentage change for each day of the year
    median_cumulative_percentage_change = yearly_cumulative_percentage_change.groupby(
        full_years_data.index.dayofyear
    ).median()

    # Remove the 366th day if present
    if 366 in median_cumulative_percentage_change.index:
        median_cumulative_percentage_change = median_cumulative_percentage_change.drop(
            index=366
        )

    # Get today's date
    today = datetime.now().date()
    # Get the current year
    current_year = datetime.now().year

    # Define the start of the current year
    start_of_year = pd.Timestamp(year=current_year, month=1, day=1, tz="UTC")

    # Filter the DataFrame to only include data from the start of the current year to now
    data_history = data[start_of_year:]
    # display(data_history)
    # Calculate year-to-date return
    year_start_price = data_history.iloc[0]["Close"]
    current_price = data_history.iloc[-1]["Close"]
    btc_ytd_return = ((current_price / year_start_price) - 1) * 100

    # Plot the median cumulative percentage change and add a horizontal line for YTD return
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=median_cumulative_percentage_change.index,
            y=median_cumulative_percentage_change.values * 100,
            mode="lines",
            name="Median Cumulative Percentage Change",
            line=dict(color="orange", width=2),
        )
    )
    # Add vertical line for today's date

    fig.add_shape(
        type="line",
        x0=today.timetuple().tm_yday,
        y0=-10,
        x1=today.timetuple().tm_yday,
        y1=130,
        line=dict(color="white", width=1.5, dash="dash"),
    )
    # Add horizontal line for YTD return

    fig.add_shape(
        type="line",
        x0=median_cumulative_percentage_change.index.min(),
        y0=btc_ytd_return,
        x1=median_cumulative_percentage_change.index.max(),
        y1=btc_ytd_return,
        line=dict(color="white", width=1.5, dash="dash"),
    )

    fig.update_layout(
        title="Median Cumulative % change of "
        + symbol
        + "$ 1D (2010 to Previous Year)",
        title_x=0.5,
        xaxis_title="Day of the Year",
        yaxis_title="Median Cumulative Percentage Change",
        plot_bgcolor="rgba(17, 17, 17, 1)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font=dict(color="white"),
        showlegend=True,
    )

    fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))

    return fig


if __name__ == "__main__":
    # Get all-time historical data from CryptoCompare API
    symbol = "ETH"
    currency = "USD"

    fig = get_mcpc_plot(symbol, currency)

    fig.show()
