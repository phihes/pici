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
            pd.read_excel("pici/tests/test_ls_labels.xlsx"),
            drop_labellers=["Test", "test"]
        ))
        assert True
    except:
        assert False


def test_stats():
    l0 = pici.labels.labels[0]
    print(f"unique cases: {l0.stats.unique_cases()}")
    print(f"total agreement:\n{l0.stats.complete_agreement()}")
    print(f"label counts:\n{l0.stats.label_counts()}")
    print(f"label counts:\n{l0.stats.label_counts(normalize=True)}")
    print(
        f"label counts:\n{l0.stats.label_counts_by_labeller(normalize=False)}")
    print(
        f"label counts:\n{l0.stats.label_counts_by_labeller(normalize=True)}")
    print(f"correlation: \n{l0.stats.label_correlation()}")
    l0.stats.plot_label_correlation()
    # l0.data.to_excel("pici/tests/test_result_labels.xlsx")


def test_ir_metrics():
    l0 = pici.labels.labels[0]
    print(f"{l0.stats.interrater_agreement()}")
    l0.set_filter("labeller=='anna+philipp' or labeller=='xwegner_lgh@outlook.de'")
    print(f"{l0.stats.interrater_agreement()}")


if __name__ == "__main__":
    pd.set_option('display.width', 80)
    # pd.set_option('expand_frame_repr', False)
    pd.set_option('display.max_columns', 999)
    test_loading()
    test_limesurvey()
    test_report()
    test_appending()
    test_stats()
    test_ir_metrics()
    print("Everything passed")
