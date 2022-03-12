from dash import dash
import dash_bootstrap_components as dbc

from dashboard import dashboard

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}]
)

if __name__ == '__main__':
    dashboard.setup(app)
    app.run_server()
