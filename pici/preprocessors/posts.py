from pici.helpers import num_words
from pici.reporting import posts_preprocessor


@posts_preprocessor
def post_position_in_thread(community):
    """
    Adds each post's position in thread (as int, starting with 1) to
    ``community.posts``.
    """
    p = community.posts.sort_values(by=[community.date_column])
    positions = p.groupby(community.topic_column).cumcount() + 1

    return positions


@posts_preprocessor
def number_of_words(community):
    """
    Adds the number of words in each post as ``int`` to ``community.posts``.
    """
    word_counts = community.posts[community.text_column].apply(num_words)

    return word_counts
