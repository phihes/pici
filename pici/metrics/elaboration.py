import numpy as np

from pici.helpers import generate_indicator_results
from pici.reporting import topics_metric


@topics_metric
def basic_text_based_elaboration(community,
     col_n_words='preprocessed_text__n_words',
     col_n_words_no_stop='preprocessed_text__n_words_no_stop',
     col_syllables='preprocessed_text__n_syllables',
     col_avg_syllables='preprocessed_text__avg_syllables_per_word',
     col_smog_index='preprocessed_text__smog_index',
     col_auto_readability='preprocessed_text__automated_readability_index',
     col_coleman_liau='preprocessed_text__coleman_liau_index',
     col_flesch_kincaid='preprocessed_text__flesch_kincaid_grade_level',
     col_frac_uppercase='preprocessed_text__frac_uppercase',
     col_frac_punctuation_marks='preprocessed_text__frac_punctuation_marks'):
    """
    Provides basic text-based elaboration indicators, such as number of
    words, number of syllables, and different readability scores.

    Args:
        col_flesch_kincaid:
        col_coleman_liau:
        col_auto_readability:
        col_smog_index:
        col_syllables: column name in community.posts to use for mean number
        of syllables
        col_n_words: column name in community.posts to use for word count
        community:

    Returns:

    """
    posts = community.posts.groupby(
        by=community.topic_column)
    initial_post = community.posts[community.posts['post_position_in_thread']
                                   == 1].groupby(by=community.topic_column)
    feedback = community.posts[community.posts['post_position_in_thread']
                                   > 1].groupby(by=community.topic_column)

    gen = lambda t, c: generate_indicator_results(posts, initial_post,
                                                  feedback, t, c)

    return {
        **gen("elaboration: number of words", col_n_words),
        **gen("elaboration: number of words (no stop words)",
            col_n_words_no_stop),
        **gen("elaboration: number of syllables", col_syllables),
        **gen("elaboration: avg. number of syllables per word",
            col_avg_syllables),
        **gen("elaboration: readability (smog)", col_smog_index),
        **gen("elaboration: readability (auto)", col_auto_readability),
        **gen("elaboration: readability (coleman-liau)", col_coleman_liau),
        **gen("elaboration: readability (flesch-kincaid)", col_flesch_kincaid),
        **gen("elaboration: fraction of uppercase characters",
            col_frac_uppercase),
        **gen("elaboration: fraction of punctuation mark characters",
                  col_frac_punctuation_marks)
    }


@topics_metric
def elaboration_based_on_topics(community):

    posts = community.posts.groupby(
        by=community.topic_column)
    initial_post = community.posts[community.posts['post_position_in_thread']
                                   == 1].groupby(by=community.topic_column)
    feedback = community.posts[community.posts['post_position_in_thread']
                                   > 1].groupby(by=community.topic_column)

    gen = lambda t, c: generate_indicator_results(posts, initial_post,
                                                  feedback, t, c)

    # TODO count total number of topics talked about in posts
    # TODO used total text to generate topic matrix

    return {
        **gen("elaboration: number of topics", 'preprocessed_text__n_topics'),
        **gen("elaboration: topics probabilities",
              'preprocessed_text__mean_topic_p')
    }