from pici.reporting import topics_preprocessor


@topics_preprocessor
def thread_text(community):
    """
    Adds column ``thread_text`` to ``community.topics``. Supplies texts of all
    posts in thread as tuple of strings in order of post creation date
    (starting with initial post).
    """

    p = community.posts.sort_values(by=[community.date_column])
    texts = p.groupby(by=community.topic_column)[
        community.text_column].apply(tuple)

    return texts