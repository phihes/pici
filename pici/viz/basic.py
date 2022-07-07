import plotly.io as pio
import plotly.express as px
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import pandas as pd

from pici.helpers import pivot

pd.options.plotting.backend = "plotly"


class BasicVisualizations:
    
    def scatter_contributors_vs_posts(self, interval='1M'):
        fig = px.scatter(
            self.pici.report.per_interval(interval=interval),
            x="number of contributors",
            y="number of posts",
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
    
    def scatter_post_per_topic_vs_elapsed_time(self):
        d = self.pici.report.topics_summary()
        d = d[d['num_posts']>1]
        d = d[['number of contributors','elapsed_days', 'community_name']]
        
        fig = px.scatter(
            d,
            x="number of contributors",
            y="elapsed_days",
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
    
    def boxplot_topics_elapsed_days(self):
        d = self.pici.report.topics_summary()
        d = d[d['num_posts']>1]
        d = d[['elapsed_days', 'community_name']]
        
        fig = px.box(
            d,
            x="elapsed_days", 
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
    
    def boxplot_topics_second_post_delay(self):
        d = self.pici.report.topics_summary()
        d = d[d['num_posts']>1]
        d = d[['second_post_delay_days', 'community_name']]
        
        fig = px.box(
            d,
            x="second_post_delay_days", 
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
    
    def boxplot_posts_number_of_words(self):
        d = self.pici.report.posts_length()
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
    
    def timeseries_number_of_posts(self, interval='1W'):
        fig = pivot(self.pici.report.per_interval(interval=interval))['number of posts'].plot()
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
    
    def timeseries_number_of_contributors(self, interval='1W'):
        fig = pivot(self.pici.report.per_interval(interval=interval))['number of contributors'].plot()
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
    
    def boxplot_number_of_contributors_per_topic(self):
    
        fig = px.box(
            self.pici.report.topics_summary()[['number of contributors', 'community_name']],
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