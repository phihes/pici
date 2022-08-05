import datetime
import glob
from abc import ABC, abstractmethod
from collections import Counter
from typing import overload
import pandas as pd
from collections import ChainMap

import pici.reporting
from pici.pipelines import Pipelines
from pici.reporting import report
from pici.datatypes import CommunityDataLevel, MetricReturnType
from pici.registries import MetricRegistry, ReportRegistry
from pici.labelling import LabelCollection

import logging
LOGGER = logging.getLogger(__name__)


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

    def __init__(self, communities, labels=[], cache_dir="cache", cache_nrows=None, start=None, end=None):
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
        self.reports = ReportRegistry(self)
        self.labels = LabelCollection(labels)
        self.pipelines = Pipelines(self)

    """
    def add_metric(self, metric):
        for c in self.communities.values():
            pici.reporting.metric.add(metric)
    """

    @overload
    def add_report(self, new_report):
        self.reports.add(new_report)

    @overload
    def add_report(self, name, list_of_metrics):
        self.reports.add_report(name, list_of_metrics)

    def generate_report(self, list_of_metrics):

        @report
        def func(communities):
            return list_of_metrics

        return func(self.communities)

    def get_metrics(self, level=None, returntype=None, unwrapped=False,
                    select_func=set.intersection):
        """
        Get all available metrics that are defined for the communities. The
        ``select_func`` parameter is set to ``set.intersection`` per
        default, meaning that only those metrics are returned, that exist
        for all communities. Metrics can be filtered by ``level`` and
        ``returntype``.

        Args:
            level:
            returntype:
            unwrapped: 'Unwrap' the returned metric functions from their
            decorator (e.g., when using as transformer in sklearn pipeline).
            select_func:

        Returns:
            dict of str:func metricname:metric

        """
        metrics = [
            c.metrics.get_all(unwrapped=unwrapped, level=level,
                              returntype=returntype)
            for cname, c in self.communities.items()
        ]
        metric_names = [
            set(m.keys()) for m in metrics
        ]
        all_metrics = dict(ChainMap(*metrics))

        return {
            name: func
            for name, func in all_metrics.items()
            if name in select_func(*metric_names)
        }


class Community(ABC):
    """
    Abstract community class.

    """

    _graph = None
    _posts = None
    _metrics = None
    _data = None

    def __init__(self, name, data, start=None, end=None, attr=None):
        if name is not None:
            self.name = name
        if attr is None:
            self._attr = self.DEFAULT_ATTRIBUTES
        else:
            self._attr = attr
        self._set_data(data, start, end)


    def date_range(self, start=None, end=None):
        return type(self).__name__(self._data, start, end)


    def timeslice(self, posts, col, start, end):
        if start is None and end is None:
            return posts
        elif start is not None and end is not None:
            return posts[(posts[col] >= start) & (posts[col] < end)]
        elif start is None and end is not None:
            return posts[posts[col] < end]
        else:
            return posts[posts[col] >= start]


    @property
    @abstractmethod
    def DEFAULT_ATTRIBUTES(self):
        raise NotImplementedError("Property not set")


    @property
    @abstractmethod
    def name(self):
        raise NotImplementedError("Property not set")

    @property
    @abstractmethod
    def date_column(self):
        raise NotImplementedError("Property not set")

    @property
    @abstractmethod
    def contributor_column(self):
        raise NotImplementedError("Property not set")

    @property
    @abstractmethod
    def topic_column(self):
        raise NotImplementedError("Property not set")

    @property
    def contributors(self):
        return self._contributors

    @property
    def posts(self):
        return self._posts

    @property
    def topics(self):
        return self._topics

    @property
    def metrics(self):
        if self._metrics is None:
            #self._metrics = CommunityMetrics(self)
            self._metrics = MetricRegistry(self)

        return self._metrics


    def contributor_by_id(self, c_id):
        return self.contributors.loc[c_id]


    def contributor_by_post_id(self, p_id):
        return self.contributors.loc[self.posts.loc[p_id].contributor_id]


    def contributors_by_topic_id(self, t_id):
        return self.topics.loc[t_id].c



    @property
    def graph(self):
        if self._graph is None:
            self._graph = self._generate_graph()

        return self._graph


    @abstractmethod
    def _generate_graph(self):
        pass


    @abstractmethod
    def _set_data(self, data, start=None, end=None):
        pass


class CommunityFactory(ABC):

    cache_date_format = '%Y-%m-%d-%H-%M-%S'


    def __init__(self, cache_dir='.', cache_nrows=None):
        self.cache_dir = cache_dir
        self.cache_nrows = cache_nrows


    def _cache_exists(self):

        files = [f'{self.cache_dir}/{self.name}_{d}_*.csv'
                 for d in self.cache_data]

        found = all([
            any(glob.iglob(f'{self.cache_dir}/{self.name}_{d}_*.csv'))
            for d in self.cache_data
        ])

        if not found:
            LOGGER.warning("Cache does not exist. Did not find some files when looking for " + ", ".join(files))

        return found

    def load_cache(self):
        cache = {
            k: glob.glob(f'{self.cache_dir}/{self.name}_{k}_*.csv')
            for k in self.cache_data
        }

        # get most recent date for which every cached file exists
        all_dates = [
            fn.split("_")[-1].split(".")[0]
            for k in cache.keys()
            for fn in cache[k]
        ]
        d_counts = Counter(all_dates)
        valid_dates = [d for d in d_counts if d_counts[d] == len(self.cache_data)]

        most_recent_date = sorted(
            valid_dates,
            key=lambda x: datetime.datetime.strptime(x, self.cache_date_format),
            reverse=True
        )[0]

        self._data = {
            k: pd.read_csv(
                f'{self.cache_dir}/{self.name}_{k}_{most_recent_date}.csv',
                nrows=self.cache_nrows
            )
            for k in self.cache_data
        }


    def add_data_to_cache(self, data):

        date_now = datetime.date.today().strftime(self.cache_date_format)

        for k, d in data.items():
            d.to_csv(f'{self.cache_dir}/{self.name}_{k}_{date_now}.csv')


    def create_community(self, name=None, use_cache=True, start=None, end=None):

        if use_cache and self._cache_exists():
            LOGGER.info("Loading community from cache...")
            self.load_cache()
        else:
            LOGGER.warning("No data in cache. Scraping community data...")
            self.scrape_data()

        return self._create_community(name, start, end)

    def load_labels(self):
        pass

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def cache_data(self):
        pass

    @abstractmethod
    def scrape_data(self):
        pass
