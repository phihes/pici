# exposed methods
import inspect

from pici.metrics import *
from pici.preprocessors import *

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

    def _exposed(self, funcname, level=None, returntype=None):
        func = self._symbol_table[funcname]
        return (
            callable(func)
            and (
                self._required_func_arg is None
                or hasattr(func, self._required_func_arg)
            )
            and (
                level is None
                or (
                    hasattr(func, 'level') and
                    getattr(func, 'level') == level
                )
            )
            and (
                returntype is None
                or (
                    hasattr(func, 'returntype') and
                    getattr(func, 'returntype') == returntype
                )
            )
        )

    def get_all(self, unwrapped=False, level=None, returntype=None):
        exposed = {}
        for funcname, func in self._symbol_table.items():
            if self._exposed(funcname, level, returntype):
                f = inspect.unwrap(func) if unwrapped else func
                exposed[funcname] = f

        return exposed

    def _call(self, funcname):
        func = self._symbol_table[funcname]
        if self._exposed(funcname):
            def newfunc(*args, **kwargs):
                return func(*args, **{**kwargs, **self._kwargs})
            return newfunc
        else:
            if not callable(func):
                raise NotImplementedError(func)
            elif (
                    (self._required_func_arg is not None)
                    and not hasattr(func, self._required_func_arg)
            ):
                raise TypeError(
                    f"Trying to call '{funcname}', which does not have "
                    f"attribute {self._required_func_arg}.")

    def add(self, func):
        self._symbol_table[func.__name__] = func


class ReportRegistry(FuncExposer):
    """
    This class exposes all methods decorated with @report as
    its own methods and passes the ``communities`` parameter to them.
    """

    def __init__(self, pici):
        super().__init__(
            required_func_arg='is_report',
            func_kwargs={'pici': pici},
            symbol_table=globals()
        )

    def add_report(self, name, list_of_metrics):

        @report
        def func(pici):
            return list_of_metrics

        self._symbol_table[name] = func


class MetricRegistry(FuncExposer):
    """
    This class exposes all methods decorated with @metric as
    its own methods and passes the ``community`` parameter to them.
    """

    def __init__(self, community):
        super().__init__(
            required_func_arg='is_metric',
            func_kwargs={'community': community},
            symbol_table=globals()
        )


class PreprocessorRegistry(FuncExposer):
    """
    This class exposes all methods decorated with @community_preprocessor as
    its own methods and passes the ``community`` parameter to them.
    """

    def __init__(self, community):
        super().__init__(
            required_func_arg='is_preprocessor',
            func_kwargs={'community': community},
            symbol_table=globals()
        )