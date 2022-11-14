import numpy as np
import networkx as nx
from functools import lru_cache

import pandas as pd

cache = lru_cache(maxsize=None)

temporal_network_metrics = {
    'in_degree_centrality': nx.in_degree_centrality
}


def _initial_post_author_network_metric(initial_post, community, metric, kind):
    """
    Get a cached network metric for the author of an initial post.

    Args:
        initial_post:
        metric:
        community:
        thread_date:
        kind:

    Returns:
        The value of the metric.
    """
    contributor = initial_post[community.contributor_column]
    thread_date = initial_post['rounded_date']
    result = np.nan
    metrics = _cached_temporal_network_metric(
        metric, community, thread_date, kind=kind)
    try:
        result = metrics[contributor]
    except KeyError:
        # contributor was not found in the network ==> metric undefined
        print(f"contributor {contributor} not found in {metric} of {kind} "
              f"network of community '{community}' on {thread_date}.")

    return result


@cache
def _cached_temporal_network_metric(metric, community, thread_date, kind):
    results = None
    graph = community.temporal_graph(
        start=None, end=thread_date, kind=kind
    )
    if graph is not None:
        try:
            metric_func = temporal_network_metrics[metric]
            results = metric_func(graph)
        except KeyError:
            raise Exception(f"The network metric {metric} is not defined.")
    else:
        print(f"warning: could not calculate {metric} for "
              f"{kind} graph (community '{community}' on {thread_date})")

    return results


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
    contributors = community.posts[community.contributor_column]
    if contributor in contributors.unique():
        posts = community.posts[contributors == contributor]
        return posts['rounded_date'].min()
    else:
        return np.nan


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

    posts = community.posts[community.posts['rounded_date'].between(
        start, end
    )]

    posts = posts[posts[community.contributor_column] == contributor]
    posts['buckets'] = posts[community.date_column].dt.round(freq='d')
    num_buckets = len(posts.buckets.unique().tolist())
    max_buckets = (end - start).days

    return num_buckets / max_buckets
