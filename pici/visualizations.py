import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import pandas as pd

pd.options.plotting.backend = "plotly"

pio.templates["peerinnovation"] = go.layout.Template({
    'layout': {
        'colorway': ['#00769B','#D67D3A', '#09B007','#E33668'],
        'font_family': "DejaVu Sans",
        'plot_bgcolor': '#E6EFF2',
        'margin': {
            'l': 0, 'r': 0, 't': 0, 'b': 0
        },
        'legend': {
            #bgcolor': '#d9d9d9'
        }
    },

})
# pio.templates.default = "ggplot2+peerinnovation"


def scatter_contributors_vs_posts(pici, interval='1M'):
    fig = px.scatter(
        pici.reports.posts_contributors_per_interval(interval=interval),
        x=f"number of contributors per {interval}",
        y=f"number of posts per {interval}",
        color="community_name",
        trendline="ols"
    )
    fig.update_layout(
        xaxis_title=f"number of contributors, interval={interval}",
        yaxis_title=f"number of posts, interval={interval}",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title=""
        )
    )
    return fig


def scatter_post_per_topic_vs_elapsed_time(pici):
    d = pici.reports.topics_summary()
    d = d[d['number of posts'] > 1]
    d = d[['number of contributors', 'delay first second post', 'community_name']]

    fig = px.scatter(
        d,
        x="number of contributors",
        y="delay first second post",
        color="community_name",
        trendline="ols",
    )
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title=""
        )
    )
    return fig


def boxplot_topics_elapsed_days(pici):
    d = pici.reports.topics_summary()
    d = d[d['number of posts'] > 1]
    # TODO: This should be total number of days since first post (not diff to second post...)
    d = d[['delay first second post', 'community_name']]

    fig = px.box(
        d,
        x="delay first second post",
        color="community_name",
        log_x=True
    )
    fig.update_layout(
        yaxis_title="",
        xaxis_title="elapsed days since first post / topic",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title=""
        )
    )
    return fig


def boxplot_topics_second_post_delay(pici):
    d = pici.reports.topics_summary()
    d = d[d['number of posts'] > 1]
    d = d[['delay first second post', 'community_name']]

    fig = px.box(
        d,
        x="delay first second post",
        color="community_name",
    )
    fig.update_layout(
        yaxis_title="",
        xaxis_title="days between first and second post / topic",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title=""
        )
    )
    return fig


def boxplot_posts_number_of_words(pici):
    d = pici.reports.post_length()
    d = d[['number of words', 'community_name']]

    fig = px.box(
        d,
        x="number of words",
        color="community_name",
    )
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title=""
        )
    )
    return fig


def timeseries_number_of_posts(pici, interval='1W'):
    fig = pici.reports.posts_contributors_per_interval(
            interval=interval
        ).pivot(
            columns="community_name"
        )[f'number of posts per {interval}'].plot()
    fig.update_layout(
        xaxis_title="",
        yaxis_title=f"number of posts / {interval}",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title=""
        )
    )
    return fig


def timeseries_number_of_contributors(pici, interval='1W'):
    fig = pici.reports.posts_contributors_per_interval(
        interval=interval
    ).pivot(
        columns="community_name"
    )[f'number of contributors per {interval}'].plot()
    fig.update_layout(
        yaxis_title=f"number of posts / {interval}",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title=""
        )
    )
    return fig


def boxplot_number_of_contributors_per_topic(pici):
    fig = px.box(
        pici.reports.topics_summary()[['number of contributors', 'community_name']],
        x="number of contributors",
        color="community_name",
        log_x=True
    )
    fig.update_layout(
        yaxis_title="",
        xaxis_title="number of contributors / topic",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title=""
        )
    )
    return fig


def scatter_lorenz_curves(pici):
    lor = pici.reports.lorenz_curve()
    fig = px.scatter(lor, x="% contributors", y="% posts", color="community_name")
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title=""
        )
    )
    return fig


def plot_lorenz_curves(pici):
    lor = pici.reports.lorenz_curve()
    fig = px.line(lor, x="% contributors", y="% posts", color="community_name")
    fig.add_shape(type='line',
                  x0=0, y0=0, x1=100, y1=100,
                  line=dict(color='Black'),
                  xref='x', yref='y'
    )
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            title=""
        )
    )
    return fig

