import functools
import pandas as pd
#from pici.reports import Reports


def join_df(func):

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        df = None
        
        # look for existing community dataframe to match stats to
        # (e.g. contributors)
        try:
            df = getattr(self._community, func.__name__.split("_")[0])
        
        # 'view' does not have df to match to
        except AttributeError:
            pass
            
        stats = func(self, *args, **kwargs)
        stats_df = None
        
        try:
            stats_df = pd.DataFrame(stats)
            
        # most likely the series' index is a mix of str and float...
        # cast indices to str, as we are dealing with names            
        except TypeError:

            _stats = {
                s: {str(i): v for i, v in row.items() }
                for s, row in stats.items()
            }
            stats_df = pd.DataFrame(_stats)
            
        return df.join(stats_df) if df is not None else stats_df

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