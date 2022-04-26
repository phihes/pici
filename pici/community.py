from abc import ABC, abstractmethod
from pici.stats import CommunityStats
import glob
import datetime
from collections import Counter
import pandas as pd
import networkx as nx
from itertools import combinations
import logging
LOGGER = logging.getLogger(__name__)


class Community(ABC):

    _graph = None
    _posts = None
    _stats = None
    _data = None
    
    def __init__(self, name, data, start=None, end=None, attr=None):
        if name is not None:
            self.name = name
        if attr is None:
            self._attr = self.DEFAULT_ATTRIBUTES
        else:
            self._attr = attr
        self._set_data(data, start, end)
        
        
    def date_range(self, start=None, end=None):
        return type(self).__name__(self._data, start, end)
    
    
    def timeslice(self, posts, col, start, end):
        if start is None and end is None:
            return posts
        elif start is not None and end is not None:
            return posts[(posts[col] >= start) & (posts[col] < end)]
        elif start is None and end is not None:
            return posts[posts[col] < end]
        else:
            return posts[posts[col] >= start]


    @property
    @abstractmethod
    def DEFAULT_ATTRIBUTES(self):
        raise NotImplementedError("Property not set")

        
    @property
    @abstractmethod
    def name(self):
        raise NotImplementedError("Property not set")
        
    @property
    @abstractmethod
    def date_column(self):
        raise NotImplementedError("Property not set")
    
    @property
    @abstractmethod
    def contributor_column(self):
        raise NotImplementedError("Property not set")
    
    @property
    @abstractmethod
    def topic_column(self):
        raise NotImplementedError("Property not set")
    
    @property
    def contributors(self):
        return self._contributors
    
    @property
    def posts(self):
        return self._posts
    
    @property
    def topics(self):
        return self._topics
    
    @property
    def stats(self):
        if self._stats is None:
            self._stats = CommunityStats(self)
            
        return self._stats
    
    
    def contributor_by_id(self, c_id):
        return self.contributors.loc[c_id]
    

    def contributor_by_post_id(self, p_id):
        return self.contributors.loc[self.posts.loc[p_id].contributor_id]
    
    
    def contributors_by_topic_id(self, t_id):
        return self.topics.loc[t_id].c
    
        

    @property
    def graph(self):
        if self._graph is None:
            self._graph = self._generate_graph()
            
        return self._graph
    
    
    @abstractmethod
    def _generate_graph(self):
        pass
    

    @abstractmethod
    def _set_data(self, data, start=None, end=None):
        pass

    
class CommunityFactory(ABC):
    
    cache_date_format = '%Y-%m-%d-%H-%M-%S'

    
    def __init__(self, cache_dir='.', cache_nrows=None):
        self.cache_dir = cache_dir
        self.cache_nrows = cache_nrows
        
        
    def _cache_exists(self):
        
        files = ['{cache}/{community}_{data}_*.csv'.format(
            cache=self.cache_dir,
            community=self.name,
            data=d)
            for d in self.cache_data]
        
        found = all([
            any(glob.iglob('{cache}/{community}_{data}_*.csv'.format(
                cache=self.cache_dir,
                community=self.name,
                data=d                
            )))
            for d in self.cache_data
        ])
        
        if not found:
            LOGGER.warning("Cache does not exist. Did not find some files when looking for " + ", ".join(files))
        
        return found
    
    def load_cache(self):
        cache = {
            k: glob.glob('{cache_dir}/{community}_{data_type}_*.csv'.format(
                    cache_dir=self.cache_dir,
                    community=self.name,
                    data_type=k                 
                )) for k in self.cache_data
        }
        
        # get most recent date for which every cached file exists
        all_dates = [
            fn.split("_")[-1].split(".")[0]
            for k in cache.keys()            
            for fn in cache[k]
        ]
        d_counts = Counter(all_dates)
        valid_dates = [d for d in d_counts if d_counts[d] == len(self.cache_data)]
        
        most_recent_date = sorted(
            valid_dates,
            key=lambda x: datetime.datetime.strptime(x, self.cache_date_format),
            reverse=True
        )[0]
            
        self._data = {
            k: pd.read_csv('{cache_dir}/{community}_{data_type}_{date}.csv'.format(
                cache_dir=self.cache_dir,
                community=self.name,
                data_type=k,
                date=most_recent_date
            ), nrows=self.cache_nrows)
            for k in self.cache_data
        }
    
    
    def add_data_to_cache(self, data):
        
        date_now = datetime.date.today().strftime(self.cache_date_format)
        
        for k,d in data.items():
            d.to_csv('{cache_dir}/{community}_{data_type}_{date}.csv'.format(
                cache_dir=self.cache_dir,
                community=self.name,
                data_type=k,
                date=date_now
            ))
                
    
    def create_community(self, name=None, use_cache=True, start=None, end=None):
                
        if use_cache and self._cache_exists():
            LOGGER.info("Loading community from cache...")
            self.load_cache()
        else:
            LOGGER.warning("No data in cache. Scraping community data...")
            self.scrape_data()
            
        return self._create_community(name, start, end)
    
    @property
    @abstractmethod
    def name(self):
        pass    
    
    @property
    @abstractmethod
    def cache_data(self):
        pass
    
    @abstractmethod
    def scrape_data(self):
        pass
    
    
def create_graph(link_data, node_data, node_col, group_col, node_attributes, connected=True):
    G = nx.Graph()
    for topic, group in link_data.groupby(group_col):
        authors = group[node_col].tolist()
        authors = set(authors)

        # create weighted edges
        for a,b in combinations(authors, 2):          
            if a and b: #and a in node_data.index and b in node_data.index and (connected or connected(a,b,topic)):
                if not G.has_node(a):
                    G.add_node(a)
                if not G.has_node(b):
                    G.add_node(b)
                if not G.has_edge(a,b):
                    G.add_edge(a,b, weight=1)
                else:
                    G[a][b]['weight'] += 1

    # add attributes to nodes
    for n, d in node_data.iterrows():
        if G.has_node(n) and n!="" and n is not None:
            for a in node_attributes:
                value = d[a] if d[a] is not None else np.nan
                G.nodes[n][a] = str(value)

    return G