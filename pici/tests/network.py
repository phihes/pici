from networkx import in_degree_centrality, degree_centrality

from pici.pici import Pici
from pici.communities.oem import OEMCommunityFactory
from pici.communities.osm import OSMCommunityFactory
from pici.communities.preciousplastic import PPCommunityFactory
import pandas as pd


pici = Pici(
    communities={
        'OpenEnergyMonitor': OEMCommunityFactory,
        'OpenStreetMap': OSMCommunityFactory,
        'PreciousPlastic': PPCommunityFactory,
    },
    start='2017-01-01',
    end='2019-01-01',
    cache_nrows=3000
)

c = pici.communities['OpenEnergyMonitor']


def test_commenter_network():
    for cm in pici.communities.values():
        g = cm.commenter_graph
        dc = in_degree_centrality(g)
        assert isinstance(dc, dict)


def test_co_contributor_network():
    for cm in pici.communities.values():
        g = cm.co_contributor_graph
        dc = degree_centrality(g)
        assert isinstance(dc, dict)


if __name__ == "__main__":
    pd.set_option('display.width', 80)
    # pd.set_option('expand_frame_repr', False)
    pd.set_option('display.max_columns', 999)
    test_commenter_network()
    test_co_contributor_network()
    print("Everything passed")