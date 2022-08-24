#import datetime
#import glob
#from abc import ABC, abstractmethod
#from collections import Counter
from typing import overload
import pandas as pd
from collections import ChainMap
from sklearn.ensemble import RandomForestClassifier
from boruta import BorutaPy
from sklearn.multiclass import OneVsRestClassifier

#import pici.reporting
from pici.communities import OEMCommunityFactory, OSMCommunityFactory, \
    PPCommunityFactory
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

    DEFAULT_COMMUNITIES = {
        'OpenEnergyMonitor': OEMCommunityFactory,
        'OpenStreetMap': OSMCommunityFactory,
        'PreciousPlastic': PPCommunityFactory,
    }

    def __init__(self, communities=None, labels=[], cache_dir="cache",
                 cache_nrows=None, start=None, end=None):
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
        if communities is None:
            communities = self.DEFAULT_COMMUNITIES
        self.communities = {
            c: f(cache_dir, cache_nrows).create_community(name=c, start=start, end=end)
            for c, f in communities.items()
        }
        self.reports = ReportRegistry(self)
        self.labels = LabelCollection(labels)
        self.pipelines = Pipelines(self)

    def add_metric(self, metric):
        for c in self.communities.values():
            c.metrics.add(metric)

    @overload
    def add_report(self, new_report):
        self.reports.add(new_report)

    @overload
    def add_report(self, name, list_of_metrics):
        self.reports.add_report(name, list_of_metrics)

    def generate_report(self, list_of_metrics):

        @report
        def func(pici):
            return list_of_metrics

        return func(pici=self)

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

    def get_topic_features(self, add_labels=True, communities=None,
                           parameters={}, keep=[]):
        pipe = self.pipelines.topics(
            parameters=parameters, keep=keep
        )
        c = self.communities
        if isinstance(communities, dict):
            c = communities
        features = pipe.transform(c).rename_axis(['id','community_name'])

        if add_labels:
            labels = self.labels.by_level(CommunityDataLevel.TOPICS)
            label_names = labels.columns.tolist()
            feature_names = features.columns.tolist()
            labelled_features = pd.merge(
                features,
                labels,
                how='inner',
                on=['id', 'community_name']
            )
            return (labelled_features[feature_names],
                    labelled_features[label_names])
        else:
            return features, None

    @staticmethod
    def select_features(self, X, y, method='boruta'):

        if method == 'boruta':

            # use numpy arrays
            X_arr = X.values
            y_arr = y.values

            rf = OneVsRestClassifier(
                RandomForestClassifier(n_jobs=-1,
                                             class_weight='balanced',
                                        max_depth=5)
            )

            feat_selector = BorutaPy(rf, n_estimators='auto', verbose=0,
                                     random_state=1)

            feat_selector.fit(X_arr, y_arr)

            confirmed = set(X.columns[feat_selector.support_])
            rejected = set(X.columns) - set(X.columns[feat_selector.support_])

            return confirmed, rejected


