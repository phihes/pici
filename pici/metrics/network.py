"""
Metrics using the community's graph object (representation of contributor network).

By level of observation:

**contributors**

- [contributor_degree][pici.metrics.network.contributor_degree]
- [contributor_centralities][pici.metrics.network.contributor_centralities]
- [contributor_communities][pici.metrics.network.contributor_communities]
"""


from pici.decorators import metric
from pici.datatypes import CommunityDataLevel, MetricReturnType
import networkx as nx
from networkx.algorithms.centrality import *
from cdlib import algorithms as cd
from cdlib import viz as cdviz

@metric(
    level=CommunityDataLevel.CONTRIBUTORS,
    returntype=MetricReturnType.DATAFRAME
)
def contributor_degree(community):
    """
    Number of contributors each contributor has co-authored with in a thread.

    Using implementation of ``networkx.Graph.degree``.

    - Data level: [``CONTRIBUTORS``][pici.datatypes.CommunityDataLevel]
    - Return type: [``DATAFRAME``][pici.datatypes.MetricReturnType]

    TODO:
        document
    Args:
        community (pici.Community):

    Returns:

    """
    return {
        'degree': dict(community.graph.degree())
    }

@metric(
    level=CommunityDataLevel.CONTRIBUTORS,
    returntype=MetricReturnType.DATAFRAME
)
def contributor_centralities(community):
    """
    Contributor centralities.

    Includes degree centrality, betweenness centrality, and eigenvector centrality.
    Using ``networkx`` implementation.

    - Data level: [``CONTRIBUTORS``][pici.datatypes.CommunityDataLevel]
    - Return type: [``DATAFRAME``][pici.datatypes.MetricReturnType]

    Args:
        community (pici.Community):

    Returns:

    """
    G = community.graph

    return {
        'degree_centrality': degree_centrality(G),
        'betweenness_centrality': betweenness_centrality(G),
        'eigenvector_centrality': eigenvector_centrality(G)
    }

@metric(
    level=CommunityDataLevel.CONTRIBUTORS,
    returntype=MetricReturnType.DATAFRAME
)
def contributor_communities(community):
    """
    Find communities within the contributor network.

    Uses weighted Leiden algorithm (Traag et al., 2018) implemented in
    ``cdlib.algorithms.leiden``. Returns a ``node: list(communities)`` representation
    using [``cdlib.NodeClustering.to_node_community_map``](https://cdlib.readthedocs.io/en/latest/reference/classes/node_clustering.html).

    Traag, Vincent, Ludo Waltman, and Nees Jan van Eck.
    [From Louvain to Leiden: guaranteeing well-connected communities.](https://arxiv.org/abs/1810.08473/)
    arXiv preprint arXiv:1810.08473 (2018).

    - Data level: [``CONTRIBUTORS``][pici.datatypes.CommunityDataLevel]
    - Return type: [``DATAFRAME``][pici.datatypes.MetricReturnType]
    Args:
        community:

    Returns:
        node_communities_map (dict of node:list(communities)): List of communities a contributor belongs to.
            See [``cdlib.NodeClustering.to_node_community_map``](https://cdlib.readthedocs.io/en/latest/reference/classes/node_clustering.html).

    """
    G = community.graph

    return {
        'leiden': cd.leiden(G, None, weights='weight').to_node_community_map()
    }