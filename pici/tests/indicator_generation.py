from pici.pici import Pici
from pici.communities.oem import OEMCommunityFactory
from pici.communities.osm import OSMCommunityFactory
from pici.communities.preciousplastic import PPCommunityFactory
import pandas as pd
import time
import cProfile
from sklearn import set_config
set_config(display="text")

pici = Pici(
    communities={
        'OpenEnergyMonitor': OEMCommunityFactory,
        'OpenStreetMap': OSMCommunityFactory,
        'PreciousPlastic': PPCommunityFactory,
    },
    start='2017-01-01',
    end='2019-01-01',
    cache_nrows=1000
)


def test_topics_indicators():
    pipe = pici.pipelines.topics()
    indicators = pipe.transform(pici.communities)
    indicators.to_excel("generated_indicators.xlsx")


if __name__ == "__main__":
    pd.set_option('display.width', 80)
    # pd.set_option('expand_frame_repr', False)
    pd.set_option('display.max_columns', 999)
    #cProfile.run('test_topics_indicators()')
    test_topics_indicators()
    print("Everything passed")
