from pici.decorators import join_df, as_table
import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px
import pandas as pd


class BasicMetrics:
    
    _report_contributors_summary = {
        "contributors_post_stats": []
    }
    
    _report_summary = {
        "community_summary": [],
    }
    
    _report_per_interval = {
        "community_posts_per_interval": ['interval'],
        "community_contributors_per_interval": ['interval'],
    }
    
    _report_topics_summary = {
        "topics_number_of_contributors": [],
        "topics_post_stats": []
    }

    
    def _poststats(self):
        posts = self._community.posts
        c_col = self._community.contributor_column
        t_col = self._community.topic_column
        d_col = self._community.date_column
        
        posts_per_topic = posts.groupby(by=[c_col, t_col]).agg('count').iloc[:,0].groupby(by=c_col)
        
        df = {
            'num_posts': posts.groupby(by=c_col).agg('count').iloc[:,0],
            'max_posts_per_topic': posts_per_topic.agg('max'),
            'avg_posts_per_topic': posts_per_topic.agg('mean'),
            'first_post': posts.groupby(by=c_col)[d_col].agg('min'),
            'last_post': posts.groupby(by=c_col)[d_col].agg('max'),
        }
        
        df["days_active"] = (df['last_post'] - df['first_post']).dt.days
                
        return df

    
    def _topicstats(self):
        posts = self._community.posts
        t_col = self._community.topic_column
        d_col = self._community.date_column
                
        df = {
            'num_posts': posts.groupby(by=t_col)[d_col].agg('count'),
            'first_post': posts.groupby(by=t_col)[d_col].agg('min'),
            'second_post': posts.groupby(by=t_col)[d_col].agg(lambda x: x.nsmallest(2).max()),
            'last_post': posts.groupby(by=t_col)[d_col].agg('max'),
        }
        
        df["elapsed_days"] = (df['last_post'] - df['first_post']).dt.days
        df["second_post_delay_days"] = (df['second_post'] - df['first_post']).dt.days
                        
        return df        
        
        
    
    @join_df
    def contributors_post_stats(self):        
        return self._poststats()
    
    @join_df
    def topics_post_stats(self):
        return self._topicstats()
    
    def contributors_plot_post_count_histogram(self):
        return px.histogram(
            self._poststats(),
            x="num_posts", 
            marginal="violin", # or violin, rug
            log_y=True
        )
    
    @as_table
    def community_summary(self):
        posts = self._community.posts
        t_col = self._community.topic_column
        c_col = self._community.contributor_column
        d_col = self._community.date_column
        
        posts_per_topic = posts.groupby(by=[c_col, t_col]).agg('count').iloc[:,0].groupby(by=c_col)
        
        return {
            'contributors': len(self._community.contributors.index),
            'posts': len(posts.index),
            'topics': len(posts.groupby(by=t_col).agg('count').index),
            'first post': posts[d_col].agg('min'),
            'last post': posts[d_col].agg('max')
        }
    

    @join_df
    def community_posts_per_interval(self, interval):
        c = self._community
        
        return {
            'number of posts': c.posts.resample(interval, on=c.date_column)[c.topic_column].count(),
        }
    
    @join_df
    def community_contributors_per_interval(self, interval):
        c = self._community

        return {
            'number of contributors': c.posts.resample(interval, on=c.date_column)[c.contributor_column].unique().apply(len)
        }
    
    
    @join_df
    def topics_number_of_contributors(self):
        c = self._community
        
        return {
            'number of contributors': c.posts.groupby(by=c.topic_column)[c.contributor_column].unique().apply(len)
        }
