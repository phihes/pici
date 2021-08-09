__version__ = '0.1.0'

from pici.stats import CommunitiesReport
from pici.viz import CommunitiesVisualizations

class Pici:
    
    def __init__(self, communities, cache_dir="cache", cache_nrows=None, start=None, end=None):
        self.communities = {
            c: f(cache_dir, cache_nrows).create_community(name=c, start=start, end=end)
            for c,f in communities.items()
        }
        self.report = CommunitiesReport(list(self.communities.values()))
        self.viz = CommunitiesVisualizations(self)