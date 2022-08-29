!!! hint "under development"
    PICI is currently under development. A first release is planned for Q4 2022.


## The PICI toolbox

**PICI** (*Peer Innovation Community Indicators*) is an open source toolbox that simplifies creating and measuring indicators of innovation in online communities. It is intended for use in a research context and allows researchers to:

<p align="right" style="float:right; margin:10px; background:#bbe7f4; padding:5px;">
    <img src="./images/pici_logo.png" width="280px" />
</p>

- automate data collection and indicator generation steps 
- simplify the implementation of new indicators
- simplify the assessment of new communities with an arbitrary "digital footprint"
- make the generation and evaluation of indicators reproducible
- provide a repository of documented & evaluated indicators of innovation in online communities

!!! info
    The toolbox is a result of the [Peer Innovation research project](https://www.peer-innovation.de/english/) by the [Chair of Innovation Economics](https://www.inno.tu-berlin.de/menue/chair_of_innovation_economics/) at [Technical University Berlin](https://www.tu.berlin/en/)  in collaboration with the [Institute for Ecological Economy Research (IÖW)](https://www.ioew.de/en/). It was financed by the [German Federal Ministry of Education and Research](https://www.bmbf.de/bmbf/en/).


## Installation

PICI is a Python package that requires Python $\geq$ 3.8. Its dependencies are managed with [Poetry](https://python-poetry.org/). To install, clone the git repository and then install the dependencies with Poetry:

```
git clone https://github.com/phihes/pici.git
cd pici
poetry install
```

## Usage

PICI is intended to use in Jupyter Notebooks (see the [examples](examples.md)). Most toolbox features are made available through the [Pici][pici.Pici] class:

``` py
from pici import Pici

p = Pici()
```

On instantiation, PICI collects data on the specified communities or loads them from cache. It can then be used to generate pre-defined indicators or to set up new indicators. PICI can represent indicator generation as a [scikit-learn pipeline](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html). This allows the usage of standard ML tools for further tasks, such as classification or indicator evaluation.

``` py
pipe = p.pipelines.topics()
pipe.transform(p.communities)
```

This documentation provides further details on other aspects, such as setting up new communities or using labeled community-data for supervised learning.

> If you are using PICI for research, please [let us know](mailto:phihes@gmail.com) and/or cite the following publication: *(upcoming)*.
