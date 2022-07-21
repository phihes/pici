from inspect import getmembers, isfunction, getfullargspec, Parameter, signature

from pici.pici import Pici
from pici.communities.oem import OEMCommunityFactory
from pici.communities.osm import OSMCommunityFactory
from pici.communities.preciousplastic import PPCommunityFactory
from pici import visualizations

import logging

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

default_values = {
    'pici': pici,
    'interval': '1M'
}


def nodef_args(func):
    sig = signature(func)
    return [
        name
        for name, param in sig.parameters.items()
        if param.default == Parameter.empty
    ]


def test_all_viz():
    for _, v in getmembers(visualizations, isfunction):
        nargs = nodef_args(v)
        missing_args = [a for a in nargs if a not in default_values.keys()]
        if len(missing_args) == 0:
            v(**{a: default_values[a] for a in nargs})
        else:
            logging.warning(
                f"Could not test {v.__name__}, missing default values for arguments {missing_args}"
            )


if __name__ == "__main__":
    test_all_viz()
    print("Everything passed")