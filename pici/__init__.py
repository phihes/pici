__version__ = '0.1.0'

# from pici.metrics import CommunitiesReport
from pici.viz import CommunitiesVisualizations
from pici.community import Community
from pici.community import CommunityFactory

__all__ = [
    'Pici', 'Community', 'CommunityFactory'
]

class Pici:
    """
    TODO:
        Add documentation.

    Examples:
        === "Python"
        ``` py
        from communities import OEMCommunityFactory, OSMCommunityFactory, PPCommunityFactory

        p = Pici(
            communities={
                'OpenEnergyMonitor': OEMCommunityFactory,
                'OpenStreetMap': OSMCommunityFactory,
                'PreciousPlastic': PPCommunityFactory,
            },
            start='2017-01-01',
            end='2017-12-01',
            cache_nrows=5000
        )
        ```
    """
    
    def __init__(self, communities, cache_dir="cache", cache_nrows=None, start=None, end=None):
        """
        Loads communities.

        Communities can be loaded from cache or scraped. Loaded data can be restricted either
        by number of rows loaded from cache (``cache_nrows``), or by setting ``start`` and
        ``end`` dates (filter on publication dates of posts).

        Args:
            communities (dict of str: pici.CommunityFactory): Dictionary of communities.
                Communities are provided as ``name (str): CommunityFactory`` tuples.
            cache_dir (str): Path to folder that contains cache files.
            cache_nrows (int): Number of rows to load from cache (None (default): load all rows).
            start (str): Start-date for filtering posts. String format must be valid input for ``pandas.Timestamp``.
            end (str): End-date for filtering posts. String format must be valid input for ``pandas.Timestamp``.
        """
        self.communities = {
            c: f(cache_dir, cache_nrows).create_community(name=c, start=start, end=end)
            for c, f in communities.items()
        }
        # self.report = CommunitiesReport(list(self.communities.values()))
        self.viz = CommunitiesVisualizations(self)