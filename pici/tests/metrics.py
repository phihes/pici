from pici import Pici
from pici.communities.oem import OEMCommunityFactory
from pici.communities.osm import OSMCommunityFactory
from pici.communities.preciousplastic import PPCommunityFactory


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


def test_basic_metrics():
    df = c.metrics.number_of_contributors_per_topic()
    # print(df)
    assert 'number of contributors' in df.columns

    tab = c.metrics.agg_number_of_posts_per_interval(interval="1d")
    print(tab)
    assert 'mean number of posts per 1d' in tab.columns

    tab2 = c.metrics.agg_posts_per_topic()
    print(tab2)
    assert 'mean posts per topic' in tab2.columns

    tab3 = c.metrics.post_dates_per_topic()
    # print(tab3)
    assert 'first post date' in tab3.columns


def test_network_metrics():
    contributors = c.metrics.contributor_degree()
    assert 'degree' in contributors.columns
    print(contributors.head(5).degree)

    c2 = c.metrics.contributor_centralities()
    assert 'degree_centrality' in c2.columns
    print(c2.head(5).degree_centrality)


if __name__ == "__main__":
    test_basic_metrics()
    test_network_metrics()
    print("Everything passed")
