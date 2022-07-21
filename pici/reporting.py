from functools import wraps

import pandas as pd

from pici.datatypes import CommunityDataLevel, MetricReturnType
from pici.helpers import FuncExposer, merge_dfs
from pici.metrics import *
from pici.decorators import report

class Report:
    pass

class ReportRegistry(FuncExposer):
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

    # def __getattr__(self, funcname):
    #     return self._call(funcname)

    def add_report(self, name, list_of_metrics,
            level=CommunityDataLevel.COMMUNITY,
            returntype=MetricReturnType.TABLE):

        @report(level=level, returntype=returntype)
        def func(communities):
            return list_of_metrics

        self._symbol_table[name] = func


class MetricRegistry(FuncExposer):
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



