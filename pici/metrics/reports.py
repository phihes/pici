"""
Reports are groups of metrics evaluated for all communities under
analysis. See also: [building reports](/guide/#building-reports).

Reports by level of observation:

**community**

- [summary][pici.metrics.reports.summary]
"""

from pici.reporting import report
from pici.metrics.basic import *
from pici.metrics.network import *
from pici.metrics.text import *


@report
def summary(pici):
    """
    Summarizes communities by posting behavior.

    Args:
        pici (pici.Pici):

    Returns:
        report:
            - number of posts,
            - number of posts per day (aggregated)
            - number of posts per month (aggregated)
    """
    return [
        (number_of_posts, {}),
        (agg_number_of_posts_per_interval, {'interval': '1d'}),
        (agg_number_of_posts_per_interval, {'interval': '1M'}),
        (agg_posts_per_topic, {})
    ]


@report
def topics_summary(pici):
    return [
        (number_of_contributors_per_topic, {}),
        (post_delays_per_topic, {}),
        (number_of_posts_per_topic, {})
    ]


@report
def posts_contributors_per_interval(pici, interval):
    """
    Number of contributors and posts for each time ``interval``.

    TODO:
        - document
        - add to TOC

    Args:
        pici:
        interval:

    Returns:
        report:
            - number of posts per ``interval``
            - number of contributors per ``interval``

    """
    return [
        (posts_per_interval, {'interval': interval}),
        (contributors_per_interval, {'interval': interval})
    ]


@report
def post_length(pici):
    return [
        (number_of_words, {}),
    ]


@report
def lorenz_curve(pici):
    return [
        (lorenz, {})
    ]