from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.graph_objs as go
import yfinance as yf

# Define a dictionary to map month numbers to names
month_names = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec",
}


current_date = datetime.now().strftime("%Y-%m-%d")

# Retrieve Bitcoin daily prices
btc = yf.download("BTC-USD", start="2010-01-01", end=current_date)

# Convert the daily prices to monthly returns
btc_monthly_returns = btc["Adj Close"].resample("M").ffill().pct_change()

# Create a DataFrame that shows year and month for each row
btc_monthly_returns_df = pd.DataFrame(btc_monthly_returns)
btc_monthly_returns_df["Year"] = btc_monthly_returns_df.index.year
btc_monthly_returns_df["Month"] = btc_monthly_returns_df.index.month
btc_monthly_returns_df["Returns"] = btc_monthly_returns_df["Adj Close"] * 100

# Pivot the DataFrame to have years as rows, months as columns, and returns as values
seasonality_df = btc_monthly_returns_df.pivot(
    index="Year", columns="Month", values="Returns"
)

# Generate hover text information
hover_text = []
for yi, yy in enumerate(seasonality_df.index):
    hover_text.append([])
    for xi, xx in enumerate(seasonality_df.columns):
        hover_text[-1].append(
            f"Year: {yy}<br>Month: {month_names[xx]}<br>Return: {seasonality_df.values[yi][xi]}%"
        )

# Use Plotly to create the heat map
fig = go.Figure(
    data=go.Heatmap(
        z=seasonality_df,
        x=[month_names[i] for i in seasonality_df.columns],
        y=seasonality_df.index,
        text=hover_text,  # Apply hover text
        hoverinfo="text",  # Display the text on hover
        hoverongaps=False,
        colorscale="Cividis",
    )
)

# Add annotations
for y, year in enumerate(seasonality_df.index):
    for m, month in enumerate(seasonality_df.columns):
        value = seasonality_df.iloc[y, m]
        # Only proceed if value is not NaN
        if not pd.isna(value):
            fig.add_annotation(
                dict(
                    font=dict(color="white"),
                    x=month_names[month],
                    y=year,
                    text=f"{value:.3}%",
                    showarrow=False,
                    xanchor="center",
                    yanchor="middle",
                )
            )

fig.update_layout(
    title="Bitcoin Monthly Returns (%) Heatmap",
    xaxis_nticks=12,
    plot_bgcolor="black",
    paper_bgcolor="black",
    font=dict(color="white"),
)
# Path to the directory where the image will be saved
plots_dir = Path("figure")

# Create the directory if it does not exist
plots_dir.mkdir(parents=True, exist_ok=True)

# Save the figure to a file (import kaleido package)
fig.write_image(
    "Bitcoin seasonality heatmap/figure/bitcoin_monthly_returns_heatmap.png"
)

fig.show()
