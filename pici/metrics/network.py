"""
Metrics using the community's graph object (representation of contributor network).

By level of observation:

**contributors**

- [contributor_degree][pici.metrics.network.contributor_degree]
- [contributor_centralities][pici.metrics.network.contributor_centralities]
- [contributor_communities][pici.metrics.network.contributor_communities]
"""
from pici.helpers import apply_to_initial_posts
from pici.reporting import metric, contributors_metric, topics_metric
from pici.datatypes import CommunityDataLevel, MetricReturnType
import networkx as nx
import numpy as np
from networkx.algorithms.centrality import *
from cdlib import algorithms as cd
from cdlib import viz as cdviz
import igraph as ig
import leidenalg


@contributors_metric
def co_contributor_degree(community):
    """
    Number of contributors each contributor has co-authored with in a thread.

    Using implementation of ``networkx.Graph.degree``.

    TODO:
        document
    Args:
        community (pici.Community):

    Returns:

    """
    return {
        'degree': dict(community.co_contributor_graph.degree())
    }


@contributors_metric
def commenter_centralities(community):
    G = community.commenter_graph

    return {
        'commenter in-degree centrality': in_degree_centrality(G),
        'commenter out-degree centrality': out_degree_centrality(G),
        'commenter betweenness centrality': betweenness_centrality(G)
    }


@contributors_metric
def co_contributor_centralities(community):
    """
    Contributor centralities.

    Includes degree centrality, betweenness centrality, and eigenvector centrality.
    Using ``networkx`` implementation.

    Args:
        community (pici.Community):

    Returns:

    """
    G = community.co_contributor_graph

    return {
        'degree_centrality': degree_centrality(G),
        'betweenness_centrality': betweenness_centrality(G),
        'eigenvector_centrality': eigenvector_centrality(G)
    }


@contributors_metric
def commenter_communities(community):
    G = community.commenter_graph

    return {
        'commenter communities: leiden': cd.leiden(G, None,
                              weights='weight').to_node_community_map()
    }


@contributors_metric
def co_contributor_communities(community, leiden_lib='cdlib'):
    """
    Find communities within the contributor network.

    Uses weighted Leiden algorithm (Traag et al., 2018) implemented in
    ``cdlib.algorithms.leiden`` or ``leidgenalg``.

    Traag, Vincent, Ludo Waltman, and Nees Jan van Eck.
    [From Louvain to Leiden: guaranteeing well-connected communities.](
    https://arxiv.org/abs/1810.08473/) arXiv preprint arXiv:1810.08473 (2018).

    Args:
        leiden_lib: Which Leiden alg. implementation to use, 'cdlib' or
        'leidenalg'
        community:

    Returns:
        node_communities_map (dict of node:list(communities)): List of
        communities a contributor belongs to. See [
        ``cdlib.NodeClustering.to_node_community_map``]
        (https://cdlib.readthedocs.io/en/latest/reference/classes
        /node_clustering.html).

    """
    G = community.co_contributor_graph

    if leiden_lib == 'cdlib':
        leiden = cd.leiden(G, None, weights='weight').to_node_community_map()
    elif leiden_lib == 'leidenalg':
        G_igraph = ig.Graph(
            len(G),
            list(zip(*list(zip(*nx.to_edgelist(G)))[:2]))
        )
        leiden = leidenalg.find_partition(
            G_igraph,
            leidenalg.ModularityVertexPartition
        )

    return {
        'co-contributor communities: leiden': leiden
    }


@topics_metric
def initiator_prestige_by_commenter_network_in_deg_centrality(community):

    degree_cache = {}

    def _c_centrality(initial_post):
        contributor = initial_post[community.contributor_column],
        thread_date = initial_post['rounded_date']
        centrality = np.nan
        if thread_date not in degree_cache.keys():
            graph = community.temporal_graph(
                start=None, end=thread_date, kind='commenter'
            )
            if graph is not None:
                in_deg_centr = nx.in_degree_centrality(graph)
                degree_cache[thread_date] = in_deg_centr
            else:
                # no network could be formed (e.g., because no posts exist
                # that match the given time-slice) ==> centrality undefined
                centrality = np.nan
        try:
            centrality = degree_cache[thread_date][contributor]
        except KeyError:
            # contributor was not found in the network ==> centrality undefined
            centrality = np.nan

        return centrality

    results = apply_to_initial_posts(community, ['_centrality'], _c_centrality)

    return {
        'initiator prestige: commenter network in-degree centrality':
            results['_centrality']
    }


@topics_metric
def initiator_centrality_in_co_contributor_network(community, k=None):

    _cache = dict()

    def centralities(initial_post):
        contributor = initial_post[community.contributor_column],
        thread_date = initial_post['rounded_date']
        _centralities = dict()

        if thread_date not in _cache.keys():
            graph = community.temporal_graph(
                start=None, end=thread_date, kind='co_contributor'
            )
            if graph is not None:
                # betweenness centrality
                betw = nx.betweenness_centrality(graph, k=k,
                                                 normalized=True,
                                                 weight='weight')
                _cache[thread_date]['betweenness'] = betw

                # closeness centrality
                close = nx.closeness_centrality(graph)
                _cache[thread_date]['closeness'] = close

        try:
            _centralities['betweenness'] = _cache[thread_date][
                'betweenness'][contributor]
        except KeyError:
            _centralities['betweenness'] = np.nan
        try:
            _centralities['closeness'] = _cache[thread_date][
                'closeness'][contributor]
        except KeyError:
            _centralities['closeness'] = np.nan

        return (_centralities['betweenness'],
                _centralities['closeness'])

    results = apply_to_initial_posts(community,
        new_cols=['betweenness','closeness'],
        func=centralities
    )

    return {
        'initiator position: betweenness centrality in co-contributor network':
            results['betweenness'],
        'initiator position: closeness centrality in co-contributor network':
            results['closeness']
    }
