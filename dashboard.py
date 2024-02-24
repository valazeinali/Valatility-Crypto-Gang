from dash import Dash, dcc, html
from z_score import get_z_score_plot
from seasonality_heatmap import get_seasonality_heatmap_plot
from s2f import get_s2f_plot
from pi_top import get_pi_top_plot

# Initialize the app
app = Dash(__name__, assets_url_path="assets")
server = app.server
app.title = "Valatility"

colors = {
    "main-background": "#111111",
    "header-text": "#ff7575",
    "sub-text": "#ffd175",
    "text": "#ff7575",
}


def send_layout():
    return html.Div(
        style={"backgroundColor": colors["main-background"]},
        children=[
            html.H1(
                children="Valatility crypto dashboard ",
                style={"textAlign": "center", "color": colors["text"]},
            ),
            html.Div(
                children=[
                    dcc.Graph(
                        id="Pi Cycle Top",
                        style={"width": "100%", "vertical-align": "middle"},
                        figure=get_pi_top_plot(symbol="BTC", currency="USD"),
                    ),
                ]
            ),
            html.Div(
                children=[
                    dcc.Graph(
                        id="Bitcoin Seasonality Heatmap",
                        style={"width": "100%", "vertical-align": "middle"},
                        figure=get_seasonality_heatmap_plot(symbol="BTC", currency="USD"),
                    ),
                ]
            ),
            html.Div(
                children=[
                    dcc.Graph(
                        id="Bitcoin S2F Heatmap",
                        style={"width": "100%", "vertical-align": "middle"},
                        figure=get_s2f_plot(symbol="BTC", currency="USD"),
                    ),
                ]
            ),
            html.Div(
                children=[
                    dcc.Graph(
                        id="Bitcoin Z-Score",
                        style={"width": "100%", "vertical-align": "middle"},
                        figure=get_z_score_plot(symbol="BTC", currency="USD"),
                    ),
                ]
            ),

            
        ],
    )


app.layout = send_layout

# Run the app
if __name__ == "__main__":
    app.run_server(port=1222)
