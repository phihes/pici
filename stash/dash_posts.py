# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_cytoscape as cyto
import plotly.express as px
import pandas as pd
import networkx as nx
from sklearn.preprocessing import MinMaxScaler

from pici.communities.osm import OSMCommunityFactory
from pici import CommunitiesReport

def scale(values, min, max):
    df = pd.DataFrame(pd.Series(values))
    scaler = MinMaxScaler((min,max))
    transformed = scaler.fit_transform(df)
    return {k:v[0] for k,v in zip(df.index,transformed)}

def networkxToCyto(G):

    #pos=nx.fruchterman_reingold_layout(G, iterations=2000, threshold=1e-10)
    #pos = nx.nx_pydot.graphviz_layout(G)
    #pos = nx.spring_layout(G)
    
    #pos = nx.nx_agraph.graphviz_layout(G, prog="neato")
    pos = {}
    deg = scale(dict(nx.degree(G, weight='weight')), 8, 50)

    nodes = [
        {
            'data': {'id': node,'size': deg[node]}, #'label': node},
            #'position': {'x': pos[node][0], 'y': pos[node][1]},
            #'locked': 'true',
        }
        for node in G.nodes
    ]
    
    edges = [
        {
            'data': {'source': x, 'target': y, 'weight': w}
        }
        for x, y, w in G.edges.data('weight', default=1)
    ]

    elements = nodes + edges

    return elements, deg


osm = OSMCommunityFactory(cache_dir="../cache", cache_nrows=10000).create_community(name="OSM (2017-2019)", start='2017-01-01', end='2020-01-01')

r = CommunitiesReport([osm])

r._report_custom = {
        "contributors_post_stats": [],
        "contributors_degree": [],
        "contributors_centralities": [],
}

contrib = r.contributors_summary(stack=True)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

elements, pos = networkxToCyto(osm.graph)

default_stylesheet = [
    {
        "selector": "node",
        "style": {
            "width": "data(size)",
            "height": "data(size)",
            "font-size": "12px",
            "text-valign": "center",
            "text-halign": "center",
            'background-color': '#BFD7B5',
            'border-width': '1px',
            'border-color': '#000000',
            'border-opacity':'0.5'
            
        }
    },
    {
        "selector": "edge",
        "style": {
            "width": 2,
            "line-color": "mapData(weight, 1, 3, blue, red)",
            "line-opacity": '0.5'
        }
    }
]

app.layout = html.Div(children=[
    html.H1(children='OpenStreetMap PeerInnovation Community'),

    #html.Div(children=str(elements)),

    dcc.Graph(
        id='num_posts',
        figure=px.box(contrib, x="community_name", y="num_posts")
    ),
    
    dcc.Graph(
        id='avg_posts_per_topic',
        figure=px.box(contrib, x="community_name", y="avg_posts_per_topic")
    ),
    
    cyto.Cytoscape(
        id='osm-user-network',
        layout={'name': 'concentric'},
        style={'width': '100%', 'height': '600px'},
        elements=elements,
        stylesheet=default_stylesheet
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)