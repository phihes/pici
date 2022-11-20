import re
import statistics

import spacy
from nltk import RegexpTokenizer
from gensim import corpora, models


import pici.community
from pici.helpers import num_words
from pici.reporting import posts_preprocessor
from textacy import preprocessing, extract, text_stats
import numpy as np
from textblob import TextBlob


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
def rounded_date(community, round_dates_to='7D'):
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
def preprocessed_text(community, n_topics=10):
    """
    This preprocessor supplies cleaned text, text statistics (using Textacy)
    and sentiment statistics (TextBlob). The following columns are added to
    ``Community.posts``:

    - clean
    - all_words
    - words_no_stop
    - n_words_no_stop
    - frac_uppercase
    - frac_punctuation_marks
    - avg_syllables_per_word
    - sentiment_polarity
    - sentiment_subjectivity
    - n_words
    - n_chars
    - n_long_words
    - n_unique_words
    - n_syllables
    - n_syllables_per_word
    - entropy
    - ttr
    - segmented_ttr
    - hdd
    - automated_index
    - flesch_reading_ease
    - smog_index
    - coleman_liau_index
    - flesch_kincaid_grade_level
    - gunning_fog_index

    Args:
        community:

    Returns:

    """

    # preprocessing

    text = community.posts[community.text_column].apply(str)
    lower_text = text.str.lower()
    clean = preprocessing.make_pipeline(
        preprocessing.remove.html_tags,
        preprocessing.replace.urls,
        preprocessing.replace.user_handles,
        preprocessing.replace.numbers,
        preprocessing.remove.accents,
        preprocessing.replace.currency_symbols,
        preprocessing.normalize.bullet_points,
        preprocessing.normalize.quotation_marks,
        #preprocessing.remove.brackets,
        preprocessing.replace.hashtags,
        preprocessing.replace.emojis,
        preprocessing.normalize.unicode,
    )
    whitespace = preprocessing.make_pipeline(
        preprocessing.normalize.whitespace
    )

    clean_text = lower_text.apply(clean).apply(
        lambda t: re.sub('[^A-Za-z0-9 ]+', ' ', t)).apply(whitespace)
    docs = clean_text.apply(nlp)

    # text statistics

    def frac_uppercase_chars(t):
        n_chars = len(t)
        if n_chars > 0:
            return len(re.findall(r'[A-Z]', t)) / n_chars
        else:
            return np.nan

    def frac_punctuation_marks(t):
        n_chars = len(t)
        if n_chars > 0:
            return len(re.findall(r'[.,;?!-]', t)) / n_chars
        else:
            return np.nan

    words_all = docs.apply(lambda t: list(extract.basics.words(t,
                    filter_stops=False)))
    words_no_stop = docs.apply(lambda t: list(extract.basics.words(t)))
    words_no_stop = words_no_stop.apply(
        lambda l: tuple(str(t) for t in l)
    )

    avg_syllables = docs.apply(lambda t: np.mean(
        text_stats.n_syllables_per_word(t)))

    sentiment = clean_text.apply(lambda t: TextBlob(t).sentiment)
    polarity = sentiment.apply(lambda s: s.polarity)
    subjectivity = sentiment.apply(lambda s: s.subjectivity)

    def get_stats(stat_funcs):
        res = []
        for f in stat_funcs:
            def safe_f(t):
                try:
                    return f(t)
                except ZeroDivisionError:
                    return np.nan
                except statistics.StatisticsError:
                    return np.nan
            res.append(
                (f.__name__, docs.apply(safe_f))
            )
        return dict(res)

    # tf-idf

    dictionary = corpora.Dictionary(words_no_stop)
    dictionary.filter_extremes(no_below=3)
    # corpus = [dictionary.doc2bow(doc) for doc in words_no_stop]
    corpus = words_no_stop.apply(dictionary.doc2bow)
    tfidf = models.TfidfModel(corpus.tolist(), dictionary=dictionary)
    corpus_tfidf = corpus.apply(lambda d: tfidf[d])

    corpus_tfidf_values = corpus_tfidf.apply(
        lambda v: tuple(e[1] for e in v))

    # topic modeling

    lda_model = models.ldamodel.LdaModel(
        corpus=corpus,
        id2word=dictionary,
        num_topics=n_topics,
        random_state=100,
        update_every=1,
        chunksize=100,
        passes=10,
        alpha='auto',
        per_word_topics=True
    )
    corpus_lda = corpus.apply(lambda d: lda_model.get_document_topics(
        bow=d,
        per_word_topics=False
    ))

    corpus_lda_topic_ids = corpus_lda.apply(lambda l: tuple(t[0] for t in l))
    corpus_lda_topic_ps = corpus_lda.apply(lambda l: tuple(t[1] for t in l))

    # print(lda_model.print_topics())
    # print('\nPerplexity: ', lda_model.log_perplexity(corpus))

    return {
        **{
            'tfidf': corpus_tfidf,
            'tfidf_sum': corpus_tfidf_values.apply(np.sum),
            'tfidf_mean': corpus_tfidf_values.apply(np.mean),
            'topics': corpus_lda,
            'topic_ids': corpus_lda_topic_ids,
            'n_topics': corpus_lda_topic_ids.apply(len),
            'topic_ps': corpus_lda_topic_ps,
            'mean_topic_p': corpus_lda_topic_ps.apply(np.mean),
            'clean': clean_text,
            'all_words': words_all,
            'words_no_stop': words_no_stop,
            'n_words_no_stop': words_no_stop.apply(len),
            'frac_uppercase': text.apply(frac_uppercase_chars),
            'frac_punctuation_marks': text.apply(frac_punctuation_marks),
            'avg_syllables_per_word': avg_syllables,
            'sentiment_polarity': polarity,
            'sentiment_subjectivity': subjectivity
        },
        **get_stats([
            text_stats.n_words,
            text_stats.n_chars,
            text_stats.n_long_words,
            text_stats.n_unique_words,
            text_stats.n_syllables,
            text_stats.n_syllables_per_word,
            text_stats.entropy,
            text_stats.diversity.ttr,
            text_stats.diversity.segmented_ttr,
            text_stats.diversity.hdd,
            text_stats.automated_readability_index,
            text_stats.readability.flesch_reading_ease,
            text_stats.readability.smog_index,
            text_stats.readability.coleman_liau_index,
            text_stats.flesch_kincaid_grade_level,
            text_stats.gunning_fog_index
        ])
    }

"""
    return {
        'clean': clean_text,
        'all_words': words_all,
        'words_no_stop': words_no_stop,
        'n_words': stats.apply(lambda t: t.n_words),
        'n_unique_words': stats.apply(lambda t: t.n_unique_words),
        'n_syllables': stats.apply(lambda t: t.n_syllables),
        'mean_syllables_per_word': stats.apply(lambda t:
                                               np.mean(
                                                   t.n_syllables_per_word)),
        'entropy': stats.apply(lambda t: t.entropy),
        'diversity_ttr': stats.apply(lambda t: t.diversity("ttr")),
        'diversity_log_ttr': stats.apply(lambda t: t.diversity("log_ttr")),
        'diversity_segmented_ttr': stats.apply(lambda t: t.diversity(
            "segmented_ttr")),
        'diversity_mtld': stats.apply(lambda t: t.diversity("mtld")),
        'diversity_hdd': stats.apply(lambda t: t.diversity("hdd"))
    }

"""
