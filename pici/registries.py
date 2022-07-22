# exposed methods
from pici.metrics import *
from pici.reporting import report


class FuncExposer:

    def __init__(self, required_func_arg=None, func_kwargs=None, symbol_table=None):
        if symbol_table is None:
            symbol_table = globals()
        if func_kwargs is None:
            func_kwargs = {}
        self._kwargs = func_kwargs
        self._required_func_arg = required_func_arg
        self._symbol_table = symbol_table

    def __getattr__(self, funcname):
        return self._call(funcname)

    def _call(self, funcname):
        func = self._symbol_table[funcname]
        if callable(func) and (
                (self._required_func_arg is None) or hasattr(func, self._required_func_arg)
        ):
            def newfunc(*args, **kwargs):
                return func(*args, **{**kwargs, **self._kwargs})
            return newfunc
        else:
            if not callable(func):
                raise NotImplementedError(func)
            elif (self._required_func_arg is not None) and not hasattr(func, self._required_func_arg):
                raise TypeError(f"Trying to call '{funcname}',"
                                f" which does not have attribute {self._required_func_arg}.")

    def add(self, func):
        self._symbol_table[func.__name__] = func


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

    def add_report(self, name, list_of_metrics):

        @report
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
