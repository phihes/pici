# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

pd.options.plotting.backend = "plotly"

df = pd.read_csv("static/df_all_communities_num_posts_per_week.csv").set_index("date")

fig = df.plot()
fig.update_layout(
    xaxis_title="",
    yaxis_title="number of contributions / week",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        title=""
    )
)

stylesheets = [
    "https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css"
]
app = dash.Dash(__name__, external_stylesheets=stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Pici'),

    dcc.Graph(
        id='contrib',
        figure=fig
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True)