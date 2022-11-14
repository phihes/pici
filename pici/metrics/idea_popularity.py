from pici.helpers import apply_to_initial_posts
from pici.reporting import topics_metric


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
