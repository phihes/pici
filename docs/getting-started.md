# Getting started

## Installation

Pici is a Python package that requires Python >= 3.8 and has several dependencies. To install, clone the git repository, install [cdlib](https://pypi.org/project/cdlib/), then install the package with [poetry](https://python-poetry.org/):

```
git clone https://github.com/phihes/pici.git
cd pici
pip install cdlib
pip install poetry
poetry install
```

## Test

## Using pici in a Jupyter notebook
=== "Python"

    ``` py
    import pandas as pd
    import plotly.io as pio
    import plotly.express as px
    import plotly.figure_factory as ff
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    import seaborn as sns
    
    pd.options.plotting.backend = "plotly"
    pio.renderers.default = "iframe"
    mpl.rcParams['figure.dpi'] = 200
    
    from pici import Pici
    from pici.communities.oem import OEMCommunityFactory
    from pici.communities.osm import OSMCommunityFactory
    from pici.communities.preciousplastic import PPCommunityFactory
    
    from pici.helpers import flat, pivot
    ```