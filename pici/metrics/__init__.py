import pandas as pd
from pici.helpers import merge_dfs
import logging
logger = logging.getLogger(__name__)

from .test import TestMetrics
from .network import NetworkMetrics
from .basic import BasicMetrics
from .text import TextMetrics


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
            logging.error('Something went wrong when looking for {}'.format(name))
            raise AttributeError 
        else:
            attr_name = self._current_view + "_" + name
            if attr_name not in dir(self):
                logging.error('Something went wrong when looking for {} in view {}'.format(name, self._current_view))
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
                    
# TODO create equivalent of "visualizers" for streamlit app
# where each "stat" is a vis.
# need class that exposes all relevant metrics
# relevant = solved using decorators?