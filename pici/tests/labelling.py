from pici.pici import Pici
from pici.communities.oem import OEMCommunityFactory
from pici.communities.osm import OSMCommunityFactory
from pici.communities.preciousplastic import PPCommunityFactory
import pandas as pd

from pici.labelling import InnovationLabels

pici = Pici(
    communities={
        'OpenEnergyMonitor': OEMCommunityFactory,
        'OpenStreetMap': OSMCommunityFactory,
        'PreciousPlastic': PPCommunityFactory,
    },
    labels=[
        InnovationLabels(
            pd.read_excel("pici/tests/test_labels.xlsx")
        )
    ],
    start='2017-01-01',
    end='2019-01-01',
    cache_nrows=3000
)

c = pici.communities['OpenEnergyMonitor']

def test_loading():
    try:
        pici.labels.add(InnovationLabels(
            pd.read_excel("pici/tests/test_labels.xlsx")
        ))
        assert False
    except:
        assert True


def test_appending():
    rep = pici.reports.topics_summary()
    assert 'label_idea' in rep.labelled_results.columns


def test_report():
    print(pici.labels)


def test_limesurvey():
    try:
        pici.labels.append(InnovationLabels().from_limesurvey(
            pd.read_excel("pici/tests/test_ls_labels.xlsx")
        ))
        assert True
    except:
        assert False


if __name__ == "__main__":
    pd.set_option('display.width', 80)
    # pd.set_option('expand_frame_repr', False)
    pd.set_option('display.max_columns', 999)
    test_loading()
    test_limesurvey()
    test_report()
    test_appending()
    print("Everything passed")