import functools
import pandas as pd
from pici.datatypes import CommunityDataLevel, MetricReturnType


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
        def wrapper(*args, **kwargs):
            community = args[0]
            metrics = func(*args, **kwargs)

            if returntype == MetricReturnType.PLAIN:
                return metrics

            elif returntype == MetricReturnType.DATAFRAME:
                try:
                    df = getattr(community, level.value)
                except AttributeError:
                    pass

                try:
                    metrics_df = pd.DataFrame(metrics)

                # most likely the series' index is a mix of str and float...
                # cast indices to str, as we are dealing with names
                except TypeError:
                    _metrics = {
                        s: {str(i): v for i, v in row.items()}
                        for s, row in metrics.items()
                    }
                    metrics_df = pd.DataFrame(_metrics)
                return df.join(metrics_df) if df is not None else metrics_df

            elif returntype == MetricReturnType.TABLE:
                metrics_table = pd.DataFrame(
                    metrics,
                    index=pd.Index([community.name], name='community_name')
                )

                return metrics_table
        wrapper.is_metric = True
        return wrapper
    return decorator

def join_df(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        df = None

        # look for existing community dataframe to match metrics to
        # (e.g. contributors)
        try:
            df = getattr(self._community, func.__name__.split("_")[0])

        # 'view' does not have df to match to
        except AttributeError:
            pass

        metrics = func(self, *args, **kwargs)
        metrics_df = None

        try:
            metrics_df = pd.DataFrame(metrics)

        # most likely the series' index is a mix of str and float...
        # cast indices to str, as we are dealing with names            
        except TypeError:

            _metrics = {
                s: {str(i): v for i, v in row.items()}
                for s, row in metrics.items()
            }
            metrics_df = pd.DataFrame(_metrics)

        return df.join(metrics_df) if df is not None else metrics_df

    return wrapper


def as_table(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        stats = func(self, *args, **kwargs)

        return pd.DataFrame(stats, index=pd.Index([self._community.name], name='community_name'))

    return wrapper


"""
def report(name, report_args=None):
    
    def _report_dec(func):

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if not name in Reports._reports.keys():
                Reports._reports[name] = {}
            Reports._reports[name][func.__name__] = report_args
            return func(self, *args, **kwargs)

        return wrapper
    
    return _report_dec
"""

"""        
        return pd.DataFrame.from_dict(
            {k:v[0].values() for k,v in summary.items()},
            orient='index',
            columns=list(list(summary.values())[0][0].keys())
        )
"""
