from pici.helpers import apply_to_initial_posts, aggregate
from pici.metrics.cached_metrics import _initial_post_author_network_metric, \
    _replies_to_own_topics
from pici.reporting import topics_metric


@topics_metric
def initiator_prestige_by_commenter_network_in_deg_centrality(community):
    """
    Determines a thread initiator's 'prestige' by their degree centrality in
    the commenter network at the time of thread creation, i.e., the number
    of users that have commented on at least one of their threads at that
    time.

    Args:
        community:

    Returns:

    """

    results = apply_to_initial_posts(community, ['_centrality'],
        lambda p: _initial_post_author_network_metric(
            p, community,
            metric='in_degree_centrality',
            kind='commenter'
        )
    )

    return {
        'initiator prestige: commenter network in-degree centrality':
            results['_centrality']
    }


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
