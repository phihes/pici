import pandas as pd
from functools import wraps
from collections.abc import Mapping

from pici.datatypes import CommunityDataLevel, MetricReturnType
from pici.helpers import merge_dfs


class Metric:
    """
    TODO: add documentation
    """

    def __init__(self, community, data, fields, level, returntype):
        self._community = community
        self._data = data
        self._fields = fields
        self._level = level
        self._returntype = returntype

    def __str__(self):
        return self.data.__str__()

    @staticmethod
    def _combine(community, metrics):
        generated_metrics = []
        fields = set()
        data = None

        # get all listed metrics' results for community
        for metric, metric_kwargs in metrics:
            m_func = getattr(community.metrics, metric.__name__)
            gen_metric = m_func(**metric_kwargs)
            generated_metrics.append(gen_metric)
            fields.update(gen_metric.fields)

        # find out what the return type is
        return_type = set([m.returntype for m in generated_metrics])
        level = set([m.level for m in generated_metrics])

        # only allow combinations of metrics with same return type and level
        if len(return_type)==1 and len(level)==1:
            return_type = list(return_type)[0]
            level = list(level)[0]
        else:
            raise Exception("Tried to combine metrics with different levels or return types")

        # How to combine results?
        #
        # case 1:
        # all metrics applied to community result in dataframes
        if all([isinstance(m.data, pd.DataFrame) for m in generated_metrics]):
            # case 1a:
            # multiple rows per community (metrics returned as dfs)
            if return_type == MetricReturnType.DATAFRAME:
                # df = merge_dfs(list(c_results), only_unique=True)
                df = merge_dfs([m.data for m in generated_metrics])
                df['community_name'] = community.name
                data = df

            # case 1b:
            # one row per community (metrics returned as table)
            elif return_type == MetricReturnType.TABLE:
                if len(generated_metrics) > 1:
                    data = merge_dfs([r.data for r in generated_metrics])
                else:
                    data = generated_metrics[0].data

        # case 2:
        # not all metrics result in dataframes
        # => put results in community: list(metrics) dictionary
        else:
            data = generated_metrics.data

        return data, level, return_type, fields

    @property
    def data(self):
        return self._data

    @property
    def fields(self):
        return self._fields

    @property
    def level(self):
        return self._level

    @property
    def returntype(self):
        return self._returntype


def metric(level: CommunityDataLevel, returntype: MetricReturnType):
    """
    A decorator for community metrics.

    The parameters ``level`` and ``type`` determine how and using which level of
    observation (topics, posts, etc.) the metrics' results are represented.

    - Only methods using this decorator are available as metrics through
    ``pici.Community.metrics``.

    Args:
        level (pici.datatypes.CommunityDataLevel): The metric's data level
            Determines to which 'view' of pici.Community metric's results
            are appended to.
        returntype (pici.datatypes.MetricReturnType): Data type of metric's return value.

    Returns:
        Returns either plain metric value, or determined value(s) appended to community data.
            Type determined by ``returntype`` parameter.
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            # community = args[0]
            community = kwargs['community']
            metric_results = func(*args, **kwargs)
            fields = set(metric_results.keys())
            metric_data = None

            if returntype == MetricReturnType.PLAIN:
                metric_data = metric_results

            elif returntype == MetricReturnType.DATAFRAME:
                df = None
                try:
                    df = getattr(community, level.value)
                except AttributeError:
                    pass

                try:
                    metrics_df = pd.DataFrame(metric_results)

                # most likely the series' index is a mix of str and float...
                # cast indices to str, as we are dealing with names
                except TypeError:
                    _metrics = {
                        s: {str(i): v for i, v in row.items()}
                        for s, row in metric_results.items()
                    }
                    metrics_df = pd.DataFrame(_metrics)

                # alt. var.: return whole df with original data...
                # return df.join(metrics_df) if df is not None else metrics_df
                # metric_data = metrics_df
                metric_data = df.join(metrics_df) if df is not None else metrics_df

            elif returntype == MetricReturnType.TABLE:
                metrics_table = pd.DataFrame(
                    metric_results,
                    index=pd.Index([community.name], name='community_name')
                )

                metric_data = metrics_table

            return Metric(community, metric_data, fields, level, returntype)

        wrapper.is_metric = True
        wrapper.level = level
        return wrapper

    return decorator


topics_metric = metric(level=CommunityDataLevel.TOPICS,
                       returntype=MetricReturnType.DATAFRAME)
posts_metric = metric(level=CommunityDataLevel.POSTS,
                      returntype=MetricReturnType.DATAFRAME)
community_metric = metric(level=CommunityDataLevel.COMMUNITY,
                          returntype=MetricReturnType.TABLE)


class Report:
    """
    TODO: add documentation
    """

    def __init__(self, pici, data, level, returntype, metric_fields):
        self._pici = pici
        self._communities = pici.communities
        self._data = data
        self._level = level
        self._returntype = returntype
        self._fields = metric_fields

    def __str__(self):
        return self.data.__str__()

    def _label(self, data):
        labels = self._pici.labels.by_level(self.level)
        data = data.rename_axis('id').reset_index()
        results = data
        if labels is not None:
            results = pd.merge(
                data,
                labels,
                how='left',
                on=['id','community_name']
            )

        return results.set_index("id")

    @property
    def data(self):
        return self._data

    @property
    def labelled_data(self):
        return self._label(self.data)

    @property
    def results(self):
        filter = set(['community_name'] + list(self.fields))
        if isinstance(self.data, pd.DataFrame):
            return self.data[filter]
        elif isinstance(self.data, Mapping):
            return {k:v for k,v in self.data.items() if k in filter}
        else:
            return self.data

    @property
    def labelled_results(self):
        return self._label(self.results)

    @property
    def level(self):
        return self._level

    @property
    def returntype(self):
        return self._returntype

    @property
    def fields(self):
        return self._fields


def report(func):
    """
    TODO: add documentation

    Args:
        func:

    Returns:

    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        pici = kwargs['pici']
        communities = pici.communities
        metric_list = func(*args, **kwargs)
        results = {cname: {} for cname in communities.keys()}
        fields = set()
        lvl = None
        rtype = None

        # call all metrics on all communities
        for cname, c in communities.items():
            d, l, r, f = Metric._combine(c, metric_list)
            results[cname] = d
            fields = f
            lvl = l
            rtype = r

        # if all results are dfs, merge down
        if rtype in [
            MetricReturnType.DATAFRAME,
            MetricReturnType.TABLE
        ]:
            results = pd.concat(list(results.values()))

        return Report(pici, results, lvl, rtype, fields)

    wrapper.is_report = True
    return wrapper
