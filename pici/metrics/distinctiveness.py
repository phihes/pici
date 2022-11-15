import numpy as np

from pici.metrics.cached_metrics import _temporal_text_similarity_dict
from pici.reporting import topics_metric


@topics_metric
def initial_post_text_distance(community,
                               similarity_metric='token_sort_ratio'):
    """
    Calculates the text distance of initial posts to previously authored
    initial posts as a measure of distinctiveness.

    Args:
        community:
        similarity_metric:
        agg_method:

    Returns:

    """

    def distance(post, agg_method):
        date = post['rounded_date']
        similarities = _temporal_text_similarity_dict(
            community, date, similarity_metric=similarity_metric,
            text_col='preprocessed_text__words_no_stop')
        text_sims = None
        try:
            text_sims = similarities[post['preprocessed_text__words_no_stop']]
        except KeyError:
            print(f"post {post['id']} not found in similarity network")
        dist = np.nan
        if text_sims is not None:
            if agg_method == 'mean':
                dist = 1 - text_sims.mean()
            elif agg_method == 'max':
                dist = 1 - text_sims.max()
            elif agg_method == 'min':
                dist = 1 - text_sims.min()

        return dist

    # select all posts at position 1 in thread (initial posts)
    initial_posts = community.posts[
        community.posts['post_position_in_thread'] == 1
    ]

    # calculate each post-text's distance to previous initial posts
    initial_posts['_distance_mean'] = initial_posts.apply(distance,
                                         agg_method='mean', axis=1)
    initial_posts['_distance_min'] = initial_posts.apply(distance,
                                         agg_method='min', axis=1)

    results = initial_posts.groupby(by=community.topic_column).first()

    return {
        f'distinctiveness: mean text-distance of initial post to previous '
        f'initial posts ({similarity_metric})': results['_distance_mean'],
        f'distinctiveness: min text-distance of initial post to previous '
        f'initial posts ({similarity_metric})': results['_distance_min'],
    }