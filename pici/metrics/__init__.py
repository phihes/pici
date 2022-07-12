from pici.helpers import FuncExposer
from pici.metrics.basic import *
from pici.metrics.network import *
from pici.metrics.text import *
from pici.metrics.reports import *


class Reports(FuncExposer):
    """
    This class exposes all (externally defined) methods decorated with @report as
    its own methods and passes the ``communities`` parameter to them.
    """

    def __init__(self, communities):
        super().__init__(
            required_func_arg='is_report',
            func_kwargs={'communities': communities},
            symbol_table=globals()
        )

    def __getattr__(self, funcname):
        return self._call(funcname)

    def add_report(self, name, list_of_metrics,
            level=CommunityDataLevel.COMMUNITY,
            returntype=MetricReturnType.TABLE):

        @report(level=level, returntype=returntype)
        def func(communities):
            return list_of_metrics

        self._symbol_table[name] = func


class Metrics(FuncExposer):
    """
    This class exposes all (externally defined) methods decorated with @metric as
    its own methods and passes the ``community`` parameter to them.
    """

    def __init__(self, community):
        super().__init__(
            required_func_arg='is_metric',
            func_kwargs={'community': community},
            symbol_table=globals()
        )

    """
    def __getattr__(self, funcname):

        
        func = globals()[funcname]
        if callable(func) and hasattr(func, 'is_metric') and func.is_metric is True:
            def newfunc(*args, **kwargs):
                return func(self._community, *args, **kwargs)
            return newfunc
        else:
            if not callable(func):
                raise NotImplementedError(func)
            elif not hasattr(func, 'is_metric'):
                raise Exception("This is not a metric. Add the @metric decorator to the method definition.")
        

        return call_if_has_attr(funcname, 'is_metric', [self._community])
    """


"""
class CommunityMetrics(
    TestMetrics,
    NetworkMetrics,
    BasicMetrics,
    TextMetrics
):
    _views = ['contributors', 'posts', 'topics', 'community', 'graph', 'communities']

    def __init__(self, community, view=None):
        self._community = community
        self._current_view = view

    def __getattr__(self, name):
        if name in self._views:
            return CommunityMetrics(self._community, name)
        elif self._current_view is None:
            logging.error(f'Something went wrong when looking for {name}')
            raise AttributeError
        else:
            attr_name = self._current_view + "_" + name
            if attr_name not in dir(self):
                logging.error(f'Something went wrong when looking for {name} in view {self._current_view}')
                raise AttributeError
            else:
                attr = getattr(self, attr_name)
                if callable(attr):
                    def newfunc(*args, **kwargs):
                        return attr(*args, **kwargs)

                    return newfunc
                else:
                    return attr


class CommunitiesReport(
    TestMetrics,
    NetworkMetrics,
    BasicMetrics,
    TextMetrics
):

    def __init__(self, communities):
        self._communities = communities

    def __getattr__(self, name):

        attr_name = "_report_" + name

        if attr_name not in dir(self):
            raise AttributeError
        else:
            def wrapper(stack=True, **kw):
                results = {c.name: {} for c in self._communities}
                attr = getattr(self, attr_name)
                merged_dfs = False
                for c in self._communities:
                    c_res = {}
                    for func_name, func_attr_names in attr.items():
                        func = getattr(c.metrics, func_name)
                        c_res[func_name] = func(**{a: kw[a] for a in func_attr_names})

                    if all([isinstance(r, pd.DataFrame) for r in c_res.values()]):
                        merged_dfs = True
                        if stack:
                            df = merge_dfs(list(c_res.values()), only_unique=True)
                            df['community_name'] = c.name
                            results[c.name] = df
                        else:
                            results[c.name] = merge_dfs(list(c_res.values()))
                    else:
                        results[c.name] = list(c_res.values())

                if merged_dfs and stack:
                    return pd.concat(list(results.values()))
                else:
                    return results

            return wrapper
            
"""

# TODO create equivalent of "visualizers" for streamlit app
# where each "stat" is a vis.
# need class that exposes all relevant metrics
# relevant = solved using decorators?
# https://discuss.streamlit.io/t/streamlit-deployment-guide-wiki/5099
