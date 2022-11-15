"""
This is a collection of all cachable functions that are used in the
calculation of indicators. The cache is implemented using
``functools.lru_cache`` with ``maxsize=None``. Caching is commonly done at
least on community level (pici.Community is hashable). Examples for when
using a cache makes sense:

- calculating the similarity of post texts (done once for all combinations)
- generating "temporal networks" (filtered representations of networks,
depending on dates of posts)

It is recommended to define cached parts of indicators here.
"""
import numpy as np
import networkx as nx
from functools import lru_cache
from textacy.representations.network import build_similarity_network
import pandas as pd

cache = lru_cache(maxsize=None)

temporal_network_metrics = {
    'in_degree_centrality': nx.in_degree_centrality,
    'out_degree_centrality': nx.out_degree_centrality
}


@cache
def _text_similarity_network(community,
                             text_col='preprocessed_text__words_no_stop',
                             similarity_metric='token_sort_ratio',
                             only_initial_posts=True):
    """
    Create a text-similarity network for all posts in community, using
    ``textacy.representations.network.build_similarity_network()``.

    Args:
        community:
        text_col:
        similarity_metric:
        only_initial_posts:

    Returns:

    """
    posts = posts = community.posts
    if only_initial_posts:
        posts = community.posts[
            community.posts['post_position_in_thread'] == 1
        ]
    texts = posts[text_col].tolist()
    g = build_similarity_network(texts, edge_weighting=similarity_metric)
    return g


@cache
def _temporal_text_similarity_network(community, date,
                                   text_col='preprocessed_text__words_no_stop',
                                   similarity_metric='token_sort_ratio',
                                   only_initial_posts=True):
    """
    Create a subview graph of the text similarity network created by
    ```_text_similarity_network()`` by filtering out all nodes (=posts)
    where post.date is > date.

    Args:
        community:
        date:
        text_col:
        similarity_metric:
        only_initial_posts:

    Returns:

    """

    # get cached text similarity network
    g = _text_similarity_network(community, text_col, similarity_metric,
                                 only_initial_posts)

    # determine which texts (=nodes) should be filtered out of network
    filtered_df = community.posts[
        community.posts['rounded_date'] <= date]
    filtered_texts = set(filtered_df[text_col].unique())

    # create filtered view
    sub_g = nx.subgraph_view(g, filter_node=lambda n: n in filtered_texts)

    return sub_g


@cache
def _temporal_text_similarity_dict(community, date,
                                   text_col='preprocessed_text__words_no_stop',
                                   similarity_metric='token_sort_ratio'):
    """
    Returns a dictionary of post-text:1xn-similarity-matrix for similarity
    subgraph filtered by date.

    Args:
        community:
        date:
        text_col:
        similarity_metric:

    Returns:

    """
    g = _temporal_text_similarity_network(community, date, text_col,
                                          similarity_metric)
    adj = nx.adjacency_matrix(g, weight='weight')
    name_to_similarities = {k: adj[i]
                            for k, i in zip(
                                g.nodes,
                                range(0, g.number_of_nodes())
                            )}

    return name_to_similarities


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
