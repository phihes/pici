%reload_ext autoreload
%autoreload 2
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