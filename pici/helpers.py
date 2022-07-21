from itertools import combinations

import networkx as nx
import nltk
import numpy as np
from functools import reduce
import pandas as pd
from bs4 import BeautifulSoup


class FuncExposer:

    def __init__(self, required_func_arg=None, func_kwargs=None, symbol_table=None):
        if symbol_table is None:
            symbol_table = globals()
        if func_kwargs is None:
            func_kwargs = {}
        self._kwargs = func_kwargs
        self._required_func_arg = required_func_arg
        self._symbol_table = symbol_table

    def __getattr__(self, funcname):
        return self._call(funcname)

    def _call(self, funcname):
        func = self._symbol_table[funcname]
        if callable(func) and (
                (self._required_func_arg is None) or hasattr(func, self._required_func_arg)
        ):
            def newfunc(*args, **kwargs):
                return func(*args, **{**kwargs, **self._kwargs})
            return newfunc
        else:
            if not callable(func):
                raise NotImplementedError(func)
            elif (self._required_func_arg is not None) and not hasattr(func, self._required_func_arg):
                raise TypeError(f"Trying to call '{funcname}',"
                                f" which does not have attribute {self._required_func_arg}.")

    def add(self, func):
        self._symbol_table[func.__name__] = func


def aggregate(series, sname):
    aggs = ['mean', 'min', 'max', 'std', 'var', 'sum']
    return {
        f'{agg} {sname}': series.agg(agg)
        for agg in aggs
    }


def num_words(text):
    """
    Counts the number of words in a text. Does account for html tags and comments
    (not included in count).

    Args:
        text (str): Text to count words in.

    Returns:
        count (int): Number of words.

    """
    if isinstance(text, str):
        bs = BeautifulSoup(text, features="html.parser")
        text = bs.get_text()
        tok = nltk.word_tokenize(text)
        return len(tok)
    else:
        return np.nan


def word_occurrences(text, words):
    """
    Counts the number of occurrences of specified ``words`` in ``text``.

    Args:
        text (str): A text with words.
        words (list of str): Words.

    Returns:
        occurrences (dict of str:int): A ``word (str), number of occurrences (int)`` dictionary

    """
    if isinstance(text, str):
        bs = BeautifulSoup(text, features="html.parser")
        text = bs.get_text()
        tok = nltk.word_tokenize(text)
        counts = nltk.FreqDist(tok)
        return {f'{w}': counts[w] or 0 for w in words}
    else:
        return {f'{w}': np.nan for w in words}


def series_most_common(series):
    c = series.value_counts()
    return c.index[0] if len(c) > 0 else np.nan


def merge_dfs(dfs, only_unique=False):
    iname = dfs[0].index.name
    duplicate_columns = set.intersection(*[set(df.columns) for df in dfs])
    unique_data = reduce(lambda left, right:
                         pd.merge(
                             left[set(left.columns) - duplicate_columns],
                             right[set(right.columns) - duplicate_columns],
                             on=iname, how='left'
                         ), dfs)

    if only_unique:
        return unique_data
    else:
        return pd.merge(dfs[0][duplicate_columns], unique_data, on=iname, how="left")


def flat(df, columns="community_name"):
    p = df.pivot(columns=columns)
    p.columns = p.columns.get_level_values(1)

    return p


"""
def pivot(df, columns="community_name"):
    return df.pivot(columns=columns)
"""


def create_graph(link_data, node_data, node_col, group_col, node_attributes, connected=True):
    G = nx.Graph()
    for topic, group in link_data.groupby(group_col):
        authors = group[node_col].tolist()
        authors = set(authors)

        # create weighted edges
        for a,b in combinations(authors, 2):
            if a and b: #and a in node_data.index and b in node_data.index and (connected or connected(a,b,topic)):
                if not G.has_node(a):
                    G.add_node(a)
                if not G.has_node(b):
                    G.add_node(b)
                if not G.has_edge(a,b):
                    G.add_edge(a,b, weight=1)
                else:
                    G[a][b]['weight'] += 1

    # add attributes to nodes
    for n, d in node_data.iterrows():
        if G.has_node(n) and n!="" and n is not None:
            for a in node_attributes:
                value = d[a] if d[a] is not None else np.nan
                G.nodes[n][a] = str(value)

    return G
