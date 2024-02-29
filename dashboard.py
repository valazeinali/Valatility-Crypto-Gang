from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from flask_caching import Cache

from mcpc import get_mcpc_plot
from pi_top import get_pi_top_plot
from s2f import get_s2f_plot
from seasonality_heatmap import get_seasonality_heatmap_plot
from z_score import get_z_score_plot

# Initialize the app
app = Dash(__name__, assets_url_path="assets")
server = app.server
app.title = "Valatility Crypto Dashboard"

# Configure cache
cache = Cache(
    app.server,
    config={
        "CACHE_TYPE": "FileSystemCache",  # Simple caching strategy, suitable for development/testing
        "CACHE_DIR": "cache",
        "CACHE_DEFAULT_TIMEOUT": 3600,  # 86,400 seconds == 24 hours
    },
)

# Define your color scheme
colors = {
    "main-background": "#111111",
    "header-text": "#ff7575",
    "sub-text": "#ffd175",
    "text": "#ff7575",
}


# Define the app layout
def send_layout():
    return html.Div(
        # Style property is commented out, can be enabled if needed.
        # style={"backgroundColor": colors["main-background"]},
        className="left_light_ball",
        children=[
            html.H1(
                children="Valatility Crypto Dashboard",
                style={"textAlign": "center"},
            ),
            html.Div(
                children=[
                    dcc.Graph(
                        id="Bitcoin Pi Cycle Top",
                        style={"width": "100%", "vertical-align": "middle"},
                        config={
                            "displaylogo": False,
                            "scrollZoom": True,
                            "modeBarButtonsToAdd": [
                                "drawline",
                                "drawopenpath",
                                "drawclosedpath",
                                "drawcircle",
                                "drawrect",
                                "eraseshape",
                            ],
                        },
                        figure={
                            "layout": {
                                "title": "Bitcoin Pi Cycle Top",
                                "plot_bgcolor": "rgba(17, 17, 17, 1)",
                                "paper_bgcolor": "rgba(0, 0, 0, 0)",
                                "font": {"color": "white"},
                            }
                        },
                    ),
                ],
            ),
            html.Div(
                children=[
                    dcc.Graph(
                        id="Bitcoin Seasonality Heatmap",
                        style={"width": "100%", "vertical-align": "middle"},
                        config={
                            "displaylogo": False,
                            "scrollZoom": True,
                            "modeBarButtonsToAdd": [
                                "drawline",
                                "drawopenpath",
                                "drawclosedpath",
                                "drawcircle",
                                "drawrect",
                                "eraseshape",
                            ],
                        },
                        figure={
                            "layout": {
                                "title": "Bitcoin Seasonality Heatmap",
                                "plot_bgcolor": "rgba(17, 17, 17, 1)",
                                "paper_bgcolor": "rgba(0, 0, 0, 0)",
                                "font": {"color": "white"},
                            }
                        },
                    ),
                ],
            ),
            html.Div(
                children=[
                    dcc.Graph(
                        id="Bitcoin S2F",
                        style={"width": "100%", "vertical-align": "middle"},
                        config={
                            "displaylogo": False,
                            "scrollZoom": True,
                            "modeBarButtonsToAdd": [
                                "drawline",
                                "drawopenpath",
                                "drawclosedpath",
                                "drawcircle",
                                "drawrect",
                                "eraseshape",
                            ],
                        },
                        figure={
                            "layout": {
                                "title": "Bitcoin S2F",
                                "plot_bgcolor": "rgba(17, 17, 17, 1)",
                                "paper_bgcolor": "rgba(0, 0, 0, 0)",
                                "font": {"color": "white"},
                            }
                        },
                    ),
                ]
            ),
            html.Div(
                children=[
                    dcc.Graph(
                        id="Bitcoin Z-Score",
                        style={"width": "100%", "vertical-align": "middle"},
                        config={
                            "displaylogo": False,
                            "scrollZoom": True,
                            "modeBarButtonsToAdd": [
                                "drawline",
                                "drawopenpath",
                                "drawclosedpath",
                                "drawcircle",
                                "drawrect",
                                "eraseshape",
                            ],
                        },
                        figure={
                            "layout": {
                                "title": "Bitcoin Z-Score",
                                "plot_bgcolor": "rgba(17, 17, 17, 1)",
                                "paper_bgcolor": "rgba(0, 0, 0, 0)",
                                "font": {"color": "white"},
                            }
                        },
                    ),
                ]
            ),
            html.Div(
                children=[
                    dcc.Graph(
                        id="Bitcoin MCPC",
                        style={"width": "100%", "vertical-align": "middle"},
                        config={
                            "displaylogo": False,
                            "scrollZoom": True,
                            "modeBarButtonsToAdd": [
                                "drawline",
                                "drawopenpath",
                                "drawclosedpath",
                                "drawcircle",
                                "drawrect",
                                "eraseshape",
                            ],
                        },
                        figure={
                            "layout": {
                                "title": "Bitcoin MCPC",
                                "plot_bgcolor": "rgba(17, 17, 17, 1)",
                                "paper_bgcolor": "rgba(0, 0, 0, 0)",
                                "font": {"color": "white"},
                            }
                        },
                    ),
                ]
            ),
            html.Button("Update Data", id="update-data", n_clicks=0),
        ],
    )


app.layout = send_layout


# Function to fetch or refresh cached data
@cache.memoize()
def get_cached_data(func, symbol="BTC", currency="USD"):
    # Assuming this function uses parameters to generate cache key and fetches data.
    return func(symbol=symbol, currency=currency)


# Callbacks to update each graph using the cached data
@app.callback(
    [
        Output("Bitcoin Pi Cycle Top", "figure"),
        Output("Bitcoin Seasonality Heatmap", "figure"),
        Output("Bitcoin S2F", "figure"),
        Output("Bitcoin Z-Score", "figure"),
        Output("Bitcoin MCPC", "figure"),
    ],
    [Input("update-data", "n_clicks")],
)
def update_graphs(n_clicks):
    if n_clicks > 0:
        # Clear the cache for these specific plots when button is clicked
        cache.delete_memoized(get_cached_data, get_pi_top_plot)
        cache.delete_memoized(get_cached_data, get_seasonality_heatmap_plot)
        cache.delete_memoized(get_cached_data, get_s2f_plot)
        cache.delete_memoized(get_cached_data, get_z_score_plot)
        cache.delete_memoized(get_cached_data, get_mcpc_plot)

    # Fetch and return the updated data for each plot
    return (
        get_cached_data(get_pi_top_plot),
        get_cached_data(get_seasonality_heatmap_plot),
        get_cached_data(get_s2f_plot),
        get_cached_data(get_z_score_plot),
        get_cached_data(get_mcpc_plot),
    )


# Run the app
if __name__ == "__main__":

    app.run_server(port=1333)
