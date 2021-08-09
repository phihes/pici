import numpy as np
from functools import reduce
import pandas as pd

def series_most_common(series):
    c = series.value_counts()
    return c.index[0] if len(c)>0 else np.nan

def merge_dfs(dfs, only_unique=False):
    iname = dfs[0].index.name
    duplicate_columns = set.intersection(*[set(df.columns) for df in dfs])
    unique_data = reduce(lambda left, right:
                    pd.merge(
                       left[set(left.columns) - duplicate_columns],
                       right[set(right.columns) - duplicate_columns],
                       on=iname, how='left'
                    ), dfs)

    if only_unique:
        return unique_data
    else:
        return pd.merge(dfs[0][duplicate_columns], unique_data, on=iname, how="left")
    
def flat(df, columns="community_name"):
    
    p = df.pivot(columns=columns)
    p.columns = p.columns.get_level_values(1)
    
    return p

def pivot(df, columns="community_name"):
    
    return df.pivot(columns=columns)