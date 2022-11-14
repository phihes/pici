"""
Basic metrics based on counts, dates etc. of posts, contributors.

By level of observation / concept:

**topics**

- [number_of_contributors_per_topic][pici.metrics.basic.number_of_contributors_per_topic]
- [post_delays_per_topic][pici.metrics.basic.post_delays_per_topic]
- [post_dates_per_topic][pici.metrics.basic.post_dates_per_topic]

**community**

- [number_of_posts][pici.metrics.basic.number_of_posts]
- [agg_number_of_posts_per_interval][pici.metrics.basic.agg_number_of_posts_per_interval]
- [agg_posts_per_topic][pici.metrics.basic.agg_posts_per_topic]
"""
import pandas as pd

from pici.reporting import metric, topics_metric, community_metric, \
    posts_metric
from pici.datatypes import CommunityDataLevel, MetricReturnType
from pici.helpers import aggregate, num_words, word_occurrences

import numpy as np


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

    return aggregate({
        "posts per topic": p
    })


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

    return aggregate({
        f"number of posts per {interval}": iv_counts
    })


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


@posts_metric
def number_of_words(community):
    """
    The number of words in a post (removing html).

    Args:
        community (pici.Community):

    Returns:
        results (dict of str:int):
            - ``number of words``
    """

    return {
        'number of words': community.posts[community.text_column].apply(
            num_words
        )
    }


@posts_metric
def posts_word_occurrence(community, words, normalize=True):
    """
    Counts the occurrence of a set of words in each post.

    Args:
        community (pici.Community):
        words (list of str): List of words to count in post texts.
        normalize (bool): Normalize occurrence count by text length.

    Returns:
        results (dict of str:int):
            - ``occurrence of <word>`` for each provided ``word``
    """

    def countw(t):
        if normalize:
            nw = num_words(t)
            return {
                k: v / nw if nw > 0 else 0
                for k, v in word_occurrences(t, words).items()
            }
        else:
            return word_occurrences(t, words)

    results = community.posts[
        community.text_column].apply(countw).apply(pd.Series)

    return {'occurrence of {c}': results[c] for c in results.columns}
