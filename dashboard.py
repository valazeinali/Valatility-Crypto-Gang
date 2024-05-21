from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from flask_caching import Cache

from mcpc import get_mcpc_plot
from pi_top import get_pi_top_plot
from s2f import get_s2f_plot
from seasonality_heatmap import get_seasonality_heatmap_plot
from z_score import get_z_score_plot
from nupl_score import get_nupl_score_plot
from rainbow_chart import get_rainbow_plot
from sharpe_ratio import get_sharpe_plot
app = Dash(__name__)
server = app.server
app.title = "Valatility Crypto Dashboard"

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <meta name="c0eb82d8c86ce702816e259a5bc9355a7a588f4e" content="c0eb82d8c86ce702816e259a5bc9355a7a588f4e" />
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
<script>
(function(__htavim){
var d = document,
    s = d.createElement('script'),
    l = d.scripts[d.scripts.length - 1];
s.settings = __htavim || {};
s.src = "\/\/burlybread.com\/d\/mGF.zDdxGGlTtWP\/3kp_v_bDmGVXJOZ\/DW0e1cMOz\/QQ4FO\/DAgkzyLQTUU\/zNNpDxgl4rOyDgQ-";
s.async = true;
l.parentNode.insertBefore(s, l);
})()
</script>
</body>
</html>
'''

cache = Cache(
    app.server,
    config={
        "CACHE_TYPE": "FileSystemCache",
        "CACHE_DIR": "cache",
        "CACHE_DEFAULT_TIMEOUT": 3600,
    },
)


def send_layout():
    return html.Div(
        className="container",
        children=[
            html.H1("Valatility Crypto Dashboard", style={"textAlign": "center"}),
            # Updated dcc.Dropdown with styled options
            dcc.Dropdown(
                id="crypto-selector",
                className="crypto-dropdown",
                options=[
                    {
                        "label": html.Span(
                            [
                                html.Img(src="/assets/bitcoin.svg", height=20),
                                html.Span(
                                    "Bitcoin (BTC)",
                                    style={"font-size": 15, "padding-left": 10},
                                ),
                            ],
                            style={"align-items": "center", "display": "flex"},
                        ),
                        "value": "BTC",
                    },
                    {
                        "label": html.Span(
                            [
                                html.Img(src="/assets/ethereum.svg", height=20),
                                html.Span(
                                    "Ethereum (ETH)",
                                    style={"font-size": 15, "padding-left": 10},
                                ),
                            ],
                            style={"align-items": "center", "display": "flex"},
                        ),
                        "value": "ETH",
                    },
                    {
                        "label": html.Span(
                            [
                                html.Img(src="/assets/solana.svg", height=20),
                                html.Span(
                                    "Solana (SOL)",
                                    style={"font-size": 15, "padding-left": 10},
                                ),
                            ],
                            style={"align-items": "center", "display": "flex"},
                        ),
                        "value": "SOL",
                    },
                    {
                        "label": html.Span(
                            [
                                html.Img(src="/assets/xrp.svg", height=20),
                                html.Span(
                                    "Ripple (XRP)",
                                    style={"font-size": 15, "padding-left": 10},
                                ),
                            ],
                            style={"align-items": "center", "display": "flex"},
                        ),
                        "value": "XRP",
                    },
                    {
                        "label": html.Span(
                            [
                                html.Img(src="/assets/bnb.svg", height=20),
                                html.Span(
                                    "Binance Coin (BNB)",
                                    style={"font-size": 15, "padding-left": 10},
                                ),
                            ],
                            style={"align-items": "center", "display": "flex"},
                        ),
                        "value": "BNB",
                    },
                    {
                        "label": html.Span(
                            [
                                html.Img(src="/assets/litecoin.svg", height=20),
                                html.Span(
                                    "Litecoin (LTC)",
                                    style={"font-size": 15, "padding-left": 10},
                                ),
                            ],
                            style={"align-items": "center", "display": "flex"},
                        ),
                        "value": "LTC",
                    },
                ],
                value="BTC",  # Default value
                clearable=False,
            ),
            html.Div(id="graphs-container"),
            html.Button("Update Data", id="update-data", n_clicks=0),
        ],
    )


app.layout = send_layout


@cache.memoize()
def get_cached_data(func, symbol="BTC", currency="USD"):
    return func(symbol=symbol, currency=currency)


@app.callback(
    Output("graphs-container", "children"),
    [Input("update-data", "n_clicks"), Input("crypto-selector", "value")],
)
def update_graphs(n_clicks, selected_crypto):
    # Assuming the necessity to fetch fresh data when "Update Data" is clicked
    if n_clicks > 0:
        cache.clear()  # Clearing the whole cache. Use delete_memoized for specific func if needed.

    if selected_crypto == "BTC":
        graphs = [
            dcc.Graph(
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
                figure=get_cached_data(get_rainbow_plot, symbol=selected_crypto),
            ),
            dcc.Graph(
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
                figure=get_cached_data(get_pi_top_plot, symbol=selected_crypto),
            ),
            dcc.Graph(
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
                figure=get_cached_data(
                    get_seasonality_heatmap_plot, symbol=selected_crypto
                ),
            ),
            dcc.Graph(
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
                figure=get_cached_data(get_sharpe_plot, symbol=selected_crypto),
            ),
            dcc.Graph(
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
                figure=get_cached_data(get_s2f_plot, symbol=selected_crypto),
            ),
            dcc.Graph(
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
                figure=get_cached_data(get_z_score_plot, symbol=selected_crypto),
            ),
            dcc.Graph(
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
                figure=get_cached_data(get_mcpc_plot, symbol=selected_crypto),
            ),
            dcc.Graph(
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
                figure=get_cached_data(get_nupl_score_plot, symbol=selected_crypto),
            ),
        ]
        return graphs
    else:
        graphs = [
             dcc.Graph(
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
                figure=get_cached_data(get_rainbow_plot, symbol=selected_crypto),
            ),
            dcc.Graph(
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
                figure=get_cached_data(get_pi_top_plot, symbol=selected_crypto),
            ),
            dcc.Graph(
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
                figure=get_cached_data(
                    get_seasonality_heatmap_plot, symbol=selected_crypto
                ),
            ),
            dcc.Graph(
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
                figure=get_cached_data(get_sharpe_plot, symbol=selected_crypto),
            ),
            dcc.Graph(
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
                figure=get_cached_data(get_z_score_plot, symbol=selected_crypto),
            ),
            dcc.Graph(
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
                figure=get_cached_data(get_mcpc_plot, symbol=selected_crypto),
            ),
            dcc.Graph(
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
                figure=get_cached_data(get_nupl_score_plot, symbol=selected_crypto),
            ),
        ]
        return graphs


if __name__ == "__main__":
    app.run_server(
        debug=True
    )  # Consider setting debug=False for production environments
