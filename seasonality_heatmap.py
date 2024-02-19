import plotly.graph_objs as go
from data.get_historical_data import get_historical_data
import numpy as np
import pandas as pd
def get_seasonality_heatmap_plot(symbol, currency):

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

    # Get all-time historical data from CryptoCompare API
    
    data = get_historical_data(symbol, currency)
    

    # Convert the daily prices to monthly returns
    data_monthly_returns = data["Close"].resample("M").ffill().pct_change()

    # Create a DataFrame that shows year and month for each row
    data_monthly_returns_df = pd.DataFrame(data_monthly_returns)
    data_monthly_returns_df["Year"] = data_monthly_returns_df.index.year
    data_monthly_returns_df["Month"] = data_monthly_returns_df.index.month
    data_monthly_returns_df["Returns"] = data_monthly_returns_df["Close"] * 100

    # Pivot the DataFrame to have years as rows, months as columns, and returns as values
    seasonality_df = data_monthly_returns_df.pivot(
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
        title=symbol + " Monthly Returns (%) Heatmap",
        xaxis_nticks=12,
        plot_bgcolor="#111111",
        paper_bgcolor="#111111",
        font=dict(color="white"),
    )
    return fig



if __name__ == "__main__":
  # Get all-time historical data from CryptoCompare API
  symbol = 'BTC'
  currency = 'USD'
  
  fig = get_seasonality_heatmap_plot(symbol, currency)
  
  fig.show()
