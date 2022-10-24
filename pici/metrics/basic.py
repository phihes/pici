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
from pici.reporting import metric, topics_metric, community_metric, contributors_metric
from pici.datatypes import CommunityDataLevel, MetricReturnType
from pici.helpers import aggregate, apply_to_initial_posts

import numpy as np
import pandas as pd
from functools import lru_cache
cache = lru_cache(maxsize=None)


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


@cache
def _threads_by_contributor(community, contributor, date_limit=None):
    """
    Get all threads initiated by contributor.

    Args:
        community:
        contributor: User name
        date_limit: Date in string format, e.g. '2020-01-15'

    Returns: A list of thread-ids where the initial post was made by the
    specified user (before the specified date_limit).

    """
    tfilter = (
            (community.posts[community.contributor_column] == contributor) &
            (community.posts['post_position_in_thread'] == 1)
    )
    if date_limit is not None:
        tfilter = (tfilter & community.posts['rounded_date'] < date_limit)
    threads = community.posts[tfilter][community.topic_column].tolist()

    return threads


@cache
def _comments_by_contributor(community, contributor, date_limit=None):
    """
    Get all threads initiated by contributor.

    Args:
        community:
        contributor: User name
        date_limit: Date in string format, e.g. '2020-01-15'

    Returns: A list of post-ids where the initial post was made by the
    specified user (before the specified date_limit).

    """
    cfilter = (
            (community.posts[community.contributor_column] == contributor) &
            (community.posts['post_position_in_thread'] > 1)
    )
    if date_limit is not None:
        cfilter = cfilter & (community.posts['rounded_date'] < date_limit)
    comments = community.posts[cfilter].index.tolist()

    return comments


@cache
def _replies_to_own_topics(community, contributor, date_limit=None):
    """
    The number of replies made to initial posts by specified
    contributor in community.

    Args:
        community:
        contributor:
        date_limit: Date in string format, e.g. '2020-01-15'

    Returns: The number of replies made to initial posts made by
    contributor. If date_limit is provided, only threads & replies posted
    before the date limit are considered.

    """

    if not pd.isna(contributor):
        threads = _threads_by_contributor(community, contributor, date_limit)
        in_threads_by_contributor = community.posts[
            community.topic_column].isin(threads)
        posted_before_limit = community.posts['rounded_date'] < \
                              date_limit if date_limit is not None else True
        replies = community.posts[in_threads_by_contributor &
                                  posted_before_limit]
        num_replies = replies.groupby(by=community.topic_column).apply(
            lambda g: len(g) - 1).tolist()

    # contributor is nan
    else:
        num_replies = [np.nan]

    return num_replies


@cache
def _date_of_first_post(community, contributor):
    posts = community.posts[community.contributor_column == contributor]
    return posts['rounded_date'].min()


@topics_metric
def number_of_replies_to_topics_initiated_by_thread_initiator(
        community, ignore_temporal_dependency=True):
    """
    Bla.

    Args:

        ignore_temporal_dependency: Whether to simple count all replies,
        instead of only those that were given before the thread was initiated.
        community:

    Returns:

    """
    """
    reply_cache = {}

    def cached_replies(p):
        k = (
            p[community.contributor_column],
            None if ignore_temporal_dependency else p['date']
        )
        try:
            return reply_cache[k]
        except KeyError:
            reply_cache[k] = _replies_to_own_topics(
                community=community,
                contributor=k[0],
                date_limit=k[1]
            )
            return reply_cache[k]

    initial_posts = community.posts[
        community.posts['post_position_in_thread'] == 1
    ]
    initial_posts['_r'] = initial_posts.apply(cached_replies, axis=1)
    """
    initial_posts = community.posts[
        community.posts['post_position_in_thread'] == 1
    ]
    initial_posts['_r'] = initial_posts.apply(
        lambda p: _replies_to_own_topics(
            community, p[community.contributor_column],
            date_limit=None if ignore_temporal_dependency else p[
                'rounded_date']
        ),
        axis=1
    )
    reply_counts = initial_posts.groupby(
        by=community.topic_column
    ).first()['_r']

    return aggregate({
        'initiator prestige: replies to topics by initial contributor':
            reply_counts
    })


@topics_metric
def initiator_experience_by_past_contributions(
        community, ignore_temporal_dependency=True):
    """

    Args:
        ignore_temporal_dependency:
        community:

    Returns:

    """
    """
    thread_cache = {}
    comment_cache = {}

    def cached_threads(p):
        k = p[community.contributor_column]
        try:
            return thread_cache[k]
        except KeyError:
            thread_cache[k] = len(_threads_by_contributor(
                community=community,
                contributor=k,
                date_limit=None if ignore_temporal_dependency else p['date']
            ))
            return thread_cache[k]

    def cached_comments(p):
        k = p[community.contributor_column]
        try:
            return comment_cache[k]
        except KeyError:
            comment_cache[k] = len(_comments_by_contributor(
                community=community,
                contributor=k,
                date_limit=None if ignore_temporal_dependency else p['date']
            ))
            return comment_cache[k]

    initial_posts = community.posts[
        community.posts['post_position_in_thread'] == 1
    ]
    num_initial_posts = initial_posts.apply(cached_threads, axis=1)
    num_comments = initial_posts.apply(cached_comments, axis=1)
    """
    # select all posts at position 1 in thread (initial posts)
    initial_posts = community.posts[
        community.posts['post_position_in_thread'] == 1
    ]
    # count number of all threads that were initiated by the author of each
    # initial post
    initial_posts['num_initial_posts'] = initial_posts.apply(
        lambda p: len(_threads_by_contributor(
            community, p[community.contributor_column],
            date_limit=None if ignore_temporal_dependency else p[
                'rounded_date']
        )),
        axis=1
    )
    # count number of all comments (=posts at position 2, 3, ...) that were
    # posted by author of each initial post
    initial_posts['num_comments'] = initial_posts.apply(
        lambda p: len(_comments_by_contributor(
            community, p[community.contributor_column],
            date_limit=None if ignore_temporal_dependency else p[
                'rounded_date']
        )),
        axis=1
    )
    # difference between date of current post and first post by same
    # contributor
    initial_posts['days_since_first_post'] = initial_posts.apply(
        lambda p: (p['rounded_date'] - _date_of_first_post(
            community, p[community.contributor_column])).dt.days
        , axis=1
    )
    # normalize counts by time since first post in days
    initial_posts['num_initial_posts_per_day'] = initial_posts[
        'num_initial_posts'].divide(initial_posts['days_since_first_post'])
    initial_posts['num_comments_per_day'] = initial_posts[
        'num_comments'].divide(initial_posts['days_since_first_post'])

    # group initial posts by thread to generate required index
    results = initial_posts.groupby(by=community.topic_column).first()

    return {
        'initiator experience: number of past initial posts': results[
            'num_initial_posts'],
        'initiator experience: number of past initial posts (per day)': results[
            'num_initial_posts_per_day'],
        'initiator experience: number of past comments': results['num_comments'],
        'initiator experience: number of past comments (per day)': results[
            'num_comments_per_day'],
        'initiator experience: days since first post': results[
            'days_since_first_post']
    }


@cache
def _contribution_regularity(community, contributor, start, end):
    """
    Get the contribution regularity of ``contributor`` as the percentage of
    days that contributor posted in the forum, between the dates ``start``
    and ``end``.

    Args:
        community:
        contributor:
        start:
        end:

    Returns:

    """

    posts = community.post[community.posts['rounded_date'].between(
        start, end
    )]

    posts = posts[community.contributor_column == contributor]
    posts['buckets'] = posts[community.date_column].round(freq='d')
    num_buckets = len(posts.buckets.unique().tolist())
    max_buckets = (end - start).dt.days

    return num_buckets / max_buckets


@topics_metric
def initiator_helpfulness_by_contribution_regularity(community,
                                                     lookback_days=100):
    """
    Calculates the contribution regularity of the initiator of each thread.
    Contribution regularity is the percentage of _past days_ in which the
    initiator posted in the forum. Past days is limited by ``lookback_days``
    parameter.

    Args:
        lookback_days:
        community:

    Returns:

    """
    # select all posts at position 1 in thread (initial posts)
    initial_posts = community.posts[
        community.posts['post_position_in_thread'] == 1
    ]
    # calculate the contribution regularity for the initial contributor
    initial_posts['_regularity'] = initial_posts.apply(
        lambda p: _contribution_regularity(
            community=community,
            contributor=p[community.contributor_column],
            start=p['rounded_date']-pd.DateOffset(days=lookback_days),
            end=p['rounded_date']
        ), axis=1
    )
    results = initial_posts.groupby(by=community.topic_column).first()

    return {
        f'initiator helpfulness: past ({lookback_days} days) contribution '
        f'regularity': results['_regularity']
    }


@topics_metric
def initiator_helpfulness_by_top_commenter_status(community, contributor,
                                                  k=90):
    """
    Calculates whether a thread's initiator has top commenter status. A 'top
    commenter' has posted more comments than the ``k``-th percentile (default:
    k=90).

    Args:
        community:
        contributor:

    Returns:

    """

    # TODO

    return {
        f'initiator helpfulness: top commenter ({k} percentile)': None
    }


@topics_metric
def initiator_helpfulness_by_foreign_thread_comment_frequency(community):
    """
    This indicator measures initiator helpfulness by the frequency of
    comments by the thread's initiator that were posted in threads with a
    different initiator ('foreign threads').

    Args:
        community:

    Returns:

    """

    # TODO

    return {
        'initiator helpfulness: comment frequency in foreign threads': None
    }


@topics_metric
def idea_popularity_by_number_of_unique_users_commenting(community):
    """

    Args:
        community:

    Returns:

    """
    def _metric(initial_post):
        tposts = community.posts[
            community.posts[community.topic_column] ==
            initial_post[community.topic_column]
        ]
        num_commenters = tposts[community.contributor_column].nunique() -1
        num_comments = len(tposts.index) -1

        return num_comments, num_commenters

    results = apply_to_initial_posts(
        community, ['num_comments', 'num_commenters'], _metric)

    return {
        'idea popularity: number of unique commenters': results[
            'num_commenters'],
        'idea popularity: number of comments': results['num_comments']
    }
