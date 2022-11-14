import spacy
from pici.helpers import num_words
from pici.reporting import posts_preprocessor
from textacy import preprocessing, extract

nlp = spacy.load("en_core_web_sm")


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


@posts_preprocessor
def rounded_date(community, round_dates_to='30D'):
    """
    Round the post dates according to specified frequency.
    If ``round_dates_to`` is None (default), this preprocessor does nothing.

    Args:
        community:
        round_dates_to: Frequency to round the initial posts'
        datetimes to, e.g., 'W' (week), 'M' (month), etc. See
        <https://pandas.pydata.org/docs/user_guide/timeseries.html
        #timeseries-offset-aliases>
        for valid aliases.
    """
    r_dates = community.posts[community.date_column]
    if round_dates_to is not None:
        r_dates = r_dates.dt.round(freq=round_dates_to)

    return r_dates


@posts_preprocessor
def preprocessed_text(community):
    text = community.posts[community.text_column].apply(str)
    text = text.str.lower()
    clean = preprocessing.make_pipeline(
        preprocessing.remove.html_tags,
        preprocessing.replace.urls,
        preprocessing.replace.user_handles,
        preprocessing.replace.numbers,
        preprocessing.replace.currency_symbols,
        preprocessing.normalize.bullet_points,
        preprocessing.normalize.quotation_marks,
        preprocessing.replace.hashtags,
        preprocessing.replace.emojis,
        preprocessing.normalize.unicode,
        preprocessing.remove.brackets,
        preprocessing.normalize.whitespace
    )

    clean_text = text.apply(clean)
    docs = clean_text.apply(nlp)

    words_all = docs.apply(lambda t: list(extract.basics.words(t,
                    filter_stops=False)))
    words_no_stop = docs.apply(lambda t: list(extract.basics.words(t)))

    return {
        'clean': clean_text,
        'all_words': words_all,
        'words_no_stop': words_no_stop,
        'num_words': words_all.apply(len),
    }

