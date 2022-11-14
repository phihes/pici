from pici.helpers import generate_indicator_results
from pici.reporting import topics_metric


@topics_metric
def posts_sentiments(community):
    posts = community.posts.groupby(
        by=community.topic_column)
    initial_post = community.posts[community.posts['post_position_in_thread']
                                   == 1].groupby(by=community.topic_column)
    feedback = community.posts[community.posts['post_position_in_thread']
                                   > 1].groupby(by=community.topic_column)

    gen = lambda t, c: generate_indicator_results(posts, initial_post,
                                                  feedback, t, c)

    return {
        **gen("sentiment: polarity", "preprocessed_text__sentiment_polarity"),
        **gen("sentiment: subjectivity",
              "preprocessed_text__sentiment_subjectivity"),
    }

