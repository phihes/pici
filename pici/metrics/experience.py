import numpy as np
import pandas as pd

from pici.helpers import apply_to_initial_posts
from pici.metrics.cached_metrics import _threads_by_contributor, \
    _comments_by_contributor, _date_of_first_post, \
    _initial_post_author_network_metric
from pici.reporting import topics_metric


@topics_metric
def initiator_experience_by_past_contributions(
        community, ignore_temporal_dependency=True,
        use_rounded_date=False):
    """

    Args:
        ignore_temporal_dependency:
        community:

    Returns:

    """
    date_col = community.date_column
    if use_rounded_date:
        date_col = 'rounded_date'

    # select all posts at position 1 in thread (initial posts)
    initial_posts = community.posts[
        community.posts['post_position_in_thread'] == 1
    ]
    # count number of all threads that were initiated by the author of each
    # initial post
    initial_posts['num_initial_posts'] = initial_posts.apply(
        lambda p: len(_threads_by_contributor(
            community, p[community.contributor_column],
            date_limit=None if ignore_temporal_dependency else p[date_col]
        )),
        axis=1
    )
    # count number of all comments (=posts at position 2, 3, ...) that were
    # posted by author of each initial post
    initial_posts['num_comments'] = initial_posts.apply(
        lambda p: len(_comments_by_contributor(
            community, p[community.contributor_column],
            date_limit=None if ignore_temporal_dependency else p[date_col]
        )),
        axis=1
    )
    # difference between date of current post and first post by same
    # contributor

    def _day_diff(c, post):
        d_fp = _date_of_first_post(
            c, post[c.contributor_column])
        diff = np.nan
        if not pd.isna(d_fp):
            diff = (post[date_col] - d_fp).days
        return diff

    initial_posts['days_since_first_post'] = initial_posts.apply(
        lambda p: _day_diff(community, p), axis=1
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


@topics_metric
def initiator_experience_by_commenter_network_out_deg_centrality(community):
    """
    Determines a thread initiator's 'experience' by their out-degree
    centrality in the commenter network at the time of thread creation,
    i.e., the number of users the initiator has 'commented on' (has replied
    to in a user's thread).

    Args:
        community:

    Returns:

    """

    results = apply_to_initial_posts(community, ['_centrality'],
        lambda p: _initial_post_author_network_metric(
            p, community,
            metric='out_degree_centrality',
            kind='commenter'
        )
    )

    return {
        'initiator experience: commenter network out-degree centrality':
            results['_centrality']
    }