import pandas as pd

from pici.metrics.cached_metrics import _contribution_regularity
from pici.reporting import topics_metric


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


#@topics_metric
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


#@topics_metric
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
