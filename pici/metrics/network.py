from pici.decorators import join_df
import networkx as nx
from networkx.algorithms.centrality import *
from cdlib import algorithms as cd
from cdlib import viz as cdviz


class NetworkMetrics:
    
    _report_contributors_graph_summary = {
        "contributors_degree": [],
        "contributors_centralities": [],
        "contributors_communities": []
    }
    
    _report_community_viz = {
        "graph_plot_leiden_communities": ["vizargs"]
    }

    
    @join_df
    def contributors_degree(self):
        return {
            'degree': dict(self._community.graph.degree())
        }

    
    @join_df
    def contributors_centralities(self):
        
        G = self._community.graph
        
        return {
            'degree_centrality': degree_centrality(G),
            #'betweenness_centrality': betweenness_centrality(G),
            #'eigenvector_centrality': eigenvector_centrality(G)
        }

    
    @join_df
    def contributors_communities(self):
        
        G = self._community.graph
        
        return {
            'leiden': cd.leiden(G, None, weights='weight').to_node_community_map()
        }

    
    def graph_plot_leiden_communities(self, vizargs):
        coms = cd.louvain(self._community.graph)
        pos = nx.spring_layout(self._community.graph)
        #return cdviz.plot_network_clusters(self._community.graph, coms, pos)
        return cdviz.plot_community_graph(self._community.graph, coms, **vizargs)