from pici.pici import Pici
from pici.communities.oem import OEMCommunityFactory
from pici.communities.osm import OSMCommunityFactory
from pici.communities.preciousplastic import PPCommunityFactory
import pandas as pd
from pici.preprocessors.posts import preprocessed_text

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


def test_preprocessing_osm():
    osm = pici.communities['OpenStreetMap']
    level, df = preprocessed_text(osm)
    print(level)
    print(df)



if __name__ == "__main__":
    pd.set_option('display.width', 80)
    # pd.set_option('expand_frame_repr', False)
    pd.set_option('display.max_columns', 999)
    test_preprocessing_osm()
    print("Everything passed")