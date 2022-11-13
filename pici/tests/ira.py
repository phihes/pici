from pici.pici import Pici
import pandas as pd

from pici.labelling import InnovationLabels

pici = Pici(
    labels=[
        InnovationLabels(
            pd.read_excel("pici/tests/test_integrated_labels.xlsx",
                          sheet_name=1),
        ),
        InnovationLabels().from_limesurvey(
            pd.read_excel("pici/tests/results-664322-815628_2022-08-16.xlsx"),
            drop_labellers=["Test","test"]
        )
    ],
    start='2017-01-01',
    end='2019-01-01',
    cache_nrows=500
)

label_stats = pici.labels.labels[0].stats


def test_ira():
    goldstandard="team"
    ira = label_stats.pairwise_interrater_agreement(goldstandard=goldstandard,
                                              min_comparisons=1).dropna()
    print(ira.columns)
    ira['kappa_ok'] = (
        (ira['% complete agreement'] > 0.5) &
        (ira['Cohen kappa'] > 0)
    )
    print(ira[['% complete agreement','Cohen kappa']])
    assert all(ira.kappa_ok.tolist())


if __name__ == "__main__":
    pd.set_option('display.width', 80)
    # pd.set_option('expand_frame_repr', False)
    pd.set_option('display.max_columns', 999)
    test_ira()
    print("Everything passed")
