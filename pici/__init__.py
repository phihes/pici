__version__ = '0.1.0'

from typing import overload

from pici.datatypes import CommunityDataLevel, MetricReturnType
from pici.metrics import Reports, report
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
        self.reports = Reports(self.communities)

    def set_labels(self, labeldata, level=CommunityDataLevel.TOPICS):

        #for c in self.communities.values():
        #    c.
        pass

    def add_metric(self, metric):
        for c in self.communities.values():
            c.metric.add(metric)

    @overload
    def add_report(self, new_report):
        self.reports.add(new_report)

    @overload
    def add_report(self, name, list_of_metrics,
                   level=CommunityDataLevel.COMMUNITY,
                   returntype=MetricReturnType.TABLE):
        self.reports.add_report(name, list_of_metrics, level, returntype)

    def generate_report(self, list_of_metrics,
                   level=CommunityDataLevel.COMMUNITY,
                   returntype=MetricReturnType.TABLE):

        @report(level=level, returntype=returntype)
        def func(communities):
            return list_of_metrics

        return func(self.communities)
