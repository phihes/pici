"""
Basic metrics based on counts, dates etc. of posts, contributors.

By level of observation:

**community**

- [number_of_posts][pici.metrics.basic.number_of_posts]
- [agg_number_of_posts_per_interval][pici.metrics.basic.agg_number_of_posts_per_interval]
- [agg_posts_per_topic][pici.metrics.basic.agg_posts_per_topic]

**topics**

- [number_of_contributors_per_topic][pici.metrics.basic.number_of_contributors_per_topic]
- [post_delays_per_topic][pici.metrics.basic.post_delays_per_topic]
- [post_dates_per_topic][pici.metrics.basic.post_dates_per_topic]
"""
import inspect

from pici.reporting import metric, topics_metric, community_metric, contributors_metric
from pici.datatypes import CommunityDataLevel, MetricReturnType
from pici.helpers import aggregate

import numpy as np
import pandas as pd
from numpy import mean, sum, max, min, std


@topics_metric
def post_delays_per_topic(community):
    """
    Delays (in days) between first and second post, and first and last post.

    Args:
        community (pici.Community):

    Returns:
       results (dict of str:int):
        - ``delay first last post``
        - ``delay first second post``

    """
    posts = community.posts
    t_col = community.topic_column
    d_col = community.date_column

    first_post = posts.groupby(by=t_col)[d_col].agg('min')
    last_post = posts.groupby(by=t_col)[d_col].agg('max')
    second_post = posts.groupby(by=t_col)[d_col].agg(lambda x: x.nsmallest(2).max())

    return {
        'delay first last post': (last_post - first_post).dt.days,
        'delay first second post': (second_post - first_post).dt.days
    }


@topics_metric
def post_dates_per_topic(community):
    """
    Date of first post, second post, and last post.

    Args:
        community (pici.Community):

    Returns:
       results (dict of str:date):
        - ``first post date``
        - ``second post date``
        - ``last post date``

    """
    posts = community.posts
    t_col = community.topic_column
    d_col = community.date_column

    first_post = posts.groupby(by=t_col)[d_col].agg('min')
    last_post = posts.groupby(by=t_col)[d_col].agg('max')
    second_post = posts.groupby(by=t_col)[d_col].agg(lambda x: x.nsmallest(2).max())

    return {
        'first post date': first_post,
        'second post date': second_post,
        'last post date': last_post
    }


@community_metric
def number_of_posts(community):
    """
    Total number of posts authored by community.

    TODO:
        document

    Args:
        community:

    Returns:

    """
    return {
        'number of posts': community.posts.shape[0]
    }


@metric(
    level=CommunityDataLevel.COMMUNITY,
    returntype=MetricReturnType.DATAFRAME
)
def posts_per_interval(community, interval):
    """
    Number of posts authored by community per time interval.

    TODO:
        - document
        - add to TOC

    Args:
        community:
        interval:

    Returns:

    """
    return {
        f'number of posts per {interval}': community.posts.resample(
            interval, on=community.date_column)[community.topic_column].count()
    }


@metric(
    level=CommunityDataLevel.COMMUNITY,
    returntype=MetricReturnType.DATAFRAME
)
def contributors_per_interval(community, interval):
    """
    Number of users that have authored at least one post in time interval.

    TODO:
        - document
        - add to TOC

    Args:
        community:
        interval:

    Returns:

    """
    return {
        f'number of contributors per {interval}': community.posts.resample(
            interval, on=community.date_column)[community.contributor_column].unique().apply(len)
    }


@community_metric
def agg_posts_per_topic(community):
    """
    Min, max, and average number of posts authored per topic.

    Args:
        community:

    Returns:
        results (dict of str:int):
            - ``<agg> posts per topic``
    """

    p = community.posts.groupby(
        by=community.topic_column)[community.date_column].count()

    return aggregate(p, "posts per topic")


@community_metric
def agg_number_of_posts_per_interval(community, interval):
    """
    Number of posts per ``interval``.

    Total number of posts in community per ``interval`` (parameter).

    Args:
        community (pici.Community):
        interval (str): The interval over which to aggregate.
            See ``pandas.Timedelta`` (<https://pandas.pydata.org/docs/user_guide/timedeltas.html>)

    Returns:
       results (dict of str:int):
        - ``number of posts per <interval>``

    """
    iv_counts = community.posts.resample(
            interval,
            on=community.date_column
    )[community.topic_column].count()

    return aggregate(iv_counts, f"number of posts per {interval}")


@topics_metric
def number_of_contributors_per_topic(community):
    """
    Number of different contributors that have authored at least one post in a thread.

    Args:
        community (pici.Community):

    Returns:
        results (dict of str: int):
            - ``number of contributors``

    """

    return {
        'number of contributors': community.posts.groupby(
            by=community.topic_column
        )[community.contributor_column].unique().apply(len)
    }


@topics_metric
def number_of_posts_per_topic(community):
    """
    Number of posts per topic.

    TODO:
        - add to toc

    Args:
        community:

    Returns:
        report:
            - number of posts

    """

    return {
        'number of posts': community.posts.groupby(
            by=community.topic_column
        ).apply(len)
    }


@metric(
    level=CommunityDataLevel.COMMUNITY,
    returntype=MetricReturnType.DATAFRAME
)
def lorenz(community):
    """
    Distribution of posts (in analogy to lorenz curve). Returns (x,y) where
    x is the (least-contributing) bottom x% of users, and y the proportion
    of posts made by them.

    Args:
        community:
            report:
                - % contributors
                - % posts
    Returns:

    """
    def lrz(posts):
        y = np.cumsum(posts).astype("float32")

        # normalize to a percentage
        y /= y.max()
        y *= 100

        # prepend a 0 to y as zero stores have zero items
        y = np.hstack((0, y))

        # get cumulative percentage of stores
        x = np.linspace(0, 100, y.size)

        return x, y

    posts_per_user = community.posts.groupby(
        by=community.contributor_column
    )[community.date_column].agg("count").sort_values(ascending=True)

    x, y = lrz(posts_per_user.dropna())

    return {
        '% contributors': x,
        '% posts': y
    }


def _replies_to_own_topics(community, contributor,
                           date_limit=None):
    """
    The average number of replies made to initial posts by specified
    contributor in community.

    Args:
        community:
        contributor:
        date_limit: Date in string format, e.g. '2020-01-15'

    Returns: The average number of replies made to initial posts made by
    contributor. If date_limit is provided, only threads initiated before the
    date limit are considered.

    """

    if not pd.isna(contributor):

        # get threads initiated by contributor
        tfilter = (
            (community.posts[community.contributor_column] == contributor) &
            (community.posts['post_position_in_thread'] == 1)
        )
        if date_limit is not None:
            tfilter = (tfilter & community.posts[
                community.date_column <= date_limit])
        threads = community.posts[tfilter][community.topic_column].tolist()

        replies = community.posts[
            community.posts[community.topic_column].isin(threads)].groupby(
                by=community.topic_column).apply(lambda g: len(g) - 1)

        num_replies = replies.tolist()

    # contributor is nan
    else:
        num_replies = [np.nan]

    return num_replies


@topics_metric
def number_of_replies_to_topics_initiated_by_thread_initiator(
        community):
    """
    Bla.

    Args:
        community:

    Returns:

    """

    initial_posts = community.posts[
        community.posts['post_position_in_thread'] == 1
    ]
    initial_posts['_avg_replies'] = initial_posts.apply(
        lambda p: _replies_to_own_topics(
            community=community,
            contributor=p[community.contributor_column]
        ),
        axis=1
    )

    reply_counts = initial_posts.groupby(
        by=community.topic_column).first()['_avg_replies']

    return aggregate(
        reply_counts,
        'prestige: replies to topics by initial contributor'
    )





