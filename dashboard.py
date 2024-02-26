from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from flask_caching import Cache

from z_score import get_z_score_plot
from seasonality_heatmap import get_seasonality_heatmap_plot
from s2f import get_s2f_plot
from pi_top import get_pi_top_plot

# Initialize the app and cache
app = Dash(__name__, assets_url_path="assets")
server = app.server
app.title = "Valatility Crypto Dashboard"

# Configure cache
cache = Cache(app.server, config={
    'CACHE_TYPE': 'FileSystemCache',   # Simple caching strategy, suitable for development/testing
    'CACHE_DIR': 'cache',
    'CACHE_DEFAULT_TIMEOUT': 86400 # 86,400 seconds == 24 hours
})

colors = {
    "main-background": "#111111",
    "header-text": "#ff7575",
    "sub-text": "#ffd175",
    "text": "#ff7575",
}

def send_layout():
    return html.Div(
        #style={"backgroundColor": colors["main-background"]},
        className="left_light_ball",
        children=[
            html.H1(
                children="Valatility Crypto Dashboard",
                style={"textAlign": "center"},
            ),
            html.Div(
                children=[
                    dcc.Graph(id="Bitcoin Pi Cycle Top", style={"width": "100%", "vertical-align": "middle"}, config= {'displaylogo': False},
                    figure={
                        'layout': {
                            'title': 'Bitcoin Pi Cycle Top',
                            'plot_bgcolor': 'rgba(17, 17, 17, 1)',
                            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                            'font': {
                                'color': 'white'
                            }
                        }
                    }),
                ],
            ),
            html.Div(
                children=[
                    dcc.Graph(id="Bitcoin Seasonality Heatmap", style={"width": "100%", "vertical-align": "middle"}, config= {'displaylogo': False},
                    figure={
                        'layout': {
                            'title': 'Bitcoin Seasonality Heatmap',
                            'plot_bgcolor': 'rgba(17, 17, 17, 1)',
                            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                            'font': {
                                'color': 'white'
                            }
                        }
                    }),
                ],
            ),
            html.Div(
                children=[
                    dcc.Graph(id="Bitcoin S2F", style={"width": "100%", "vertical-align": "middle"}, config= {'displaylogo': False},
                    figure={
                        'layout': {
                            'title': 'Bitcoin S2F',
                            'plot_bgcolor': 'rgba(17, 17, 17, 1)',
                            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                            'font': {
                                'color': 'white'
                            }
                        }
                    }),
                ]
            ),
            html.Div(
                children=[
                    dcc.Graph(id="Bitcoin Z-Score", style={"width": "100%", "vertical-align": "middle"}, config= {'displaylogo': False},
                    figure={
                        'layout': {
                            'title': 'Bitcoin Z-Score',
                            'plot_bgcolor': 'rgba(17, 17, 17, 1)',
                            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                            'font': {
                                'color': 'white'
                            }
                        }
                    }),
                ]
            ),
            # Force update button, in case users want to refresh data manually before cache timeout
            html.Button('Update Data', id='update-data', n_clicks=0)
            
        ],
    )

app.layout = send_layout

# Cache and serve each plot data
@cache.memoize()
def get_cached_data(func, symbol="BTC", currency="USD"):
    # Based on the passed function, return the appropriate plot figure
    return func(symbol=symbol, currency=currency)

# Callbacks to update each graph using the cached data
@app.callback(
    [Output("Bitcoin Pi Cycle Top", "figure"),
    Output("Bitcoin Seasonality Heatmap", "figure"),
    Output("Bitcoin S2F", "figure"),
    Output("Bitcoin Z-Score", "figure")],
    [Input("update-data", "n_clicks")]
)
def update_graphs(n_clicks):
    return (
        get_cached_data(get_pi_top_plot),
        get_cached_data(get_seasonality_heatmap_plot),
        get_cached_data(get_s2f_plot),
        get_cached_data(get_z_score_plot)
    )

# Run the app
if __name__ == "__main__":
    app.run_server(port=1333)
