from pici.helpers import create_co_contributor_graph, create_commenter_graph
import pandas as pd
import scrapy
from scrapyscript import Job, Processor
import numpy as np
import json
from urllib.parse import urlparse
from pici import helpers, Community, CommunityFactory
import logging
LOGGER = logging.getLogger(__name__)


class DiscourseCommunity(Community):
    
    name = "Discourse Community"
    date_column = "date"
    contributor_column = "username"
    topic_column = "topic_slug"
    text_column = "cooked"
    
    DEFAULT_ATTRIBUTES = {
        "node_data": [
            'author_from',
            'author_type',
            'author_registered_date',
            'forum_title',
            'topic_title'
        ],
        "original_date_column": "created_at"
    }
    
    
    def _set_data(self, data, start, end):
        
        d = {}
        
        if 'posts' in data.keys():
            if isinstance(data['posts'], pd.DataFrame):
                p = data["posts"]
                
                p["date"] = pd.to_datetime(p[self._attr["original_date_column"]])
                
                d["posts"] = self.timeslice(p, self.date_column, start, end)
            else:
                raise TypeError("posts are not a pandas dataframe")
        else:
            raise ValueError("posts are missing in data")
            
        if 'users' in data.keys():
            if isinstance(data['users'], pd.DataFrame):
                c = data["users"]
                relevant_users = d["posts"][self.contributor_column]
                d["contributors"] = c[c[self.contributor_column].isin(relevant_users.tolist())].set_index(self.contributor_column)
            else:
                raise TypeError("users are not a pandas dataframe")
        else:
            raise ValueError("users are missing in data")
            
        if 'topics' in data.keys():
            if isinstance(data['topics'], pd.DataFrame):
                
                tp = data["topics"].rename(
                    columns={"slug":self.topic_column}
                ).drop(['Unnamed: 0'], axis=1).drop_duplicates(subset=['id'])
                               
                relevant_topics = d["posts"][self.topic_column]
                d["topics"] = tp[tp[self.topic_column].isin(relevant_topics.tolist())].set_index(self.topic_column)
                
                #TODO any data trafos?                
            else:
                raise TypeError("topics are not a pandas dataframe")
        else:
            raise ValueError("topics are missing in data")
            
        self._data = d
        self._posts = d['posts']
        self._contributors = d['contributors']
        self._topics = d['topics']
        
    
    def _generate_co_contributor_graph(self):
        return create_co_contributor_graph(
            self.posts,
            self.contributors,
            self.contributor_column,
            self.topic_column,
            self.contributors.columns
        )

    def _generate_commenter_graph(self):
        return create_commenter_graph(
            self.posts,
            self.contributors,
            self.contributor_column,
            self.topic_column,
            self.contributors.columns
        )
    
    
    
class DiscourseCommunityFactory(CommunityFactory):
    
    name = "discourse"
    cache_data = ['posts','users','topics']
    base_url = None
    scraping_urls = {
        "topics": "top/all.json",
        "topic": "t/{}.json",
        "user": "u/{}.json",
        "post": "t/{}/{}.json"
    }
    
    
    def _create_community(self, name, start, end):
        try:
            self._data
        except:
            raise Exception("No community data found, can not set up community.")
            
        return DiscourseCommunity(name, self._data, start, end)
    
    
    def scrape_data(self):
        
        raise NotImplementedError
        
        #processor = Processor(settings=None)
        
        # TODO 1) get topics
        # posts = pd.DataFrame(processor.run(Job(DiscourseTopicSpider)))
        
        #TODO pass base_url, scraping_urls to spiders
        #TODO pass results to subsequent runs
        #TODO create property <topics> in Community?
        
        
        #self._data = {
        #    'posts': posts
        #}
        #self.add_data_to_cache({
        #    'posts': posts
        #})       
        

# run with
# -a baseUrl=http://.../categories
class DiscourseTopicSpider(scrapy.Spider):
    
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 0.25,
        'AUTOTHROTTLE_MAX_DELAY': 0.5,
        'DOWNLOAD_DELAY': 0.25,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1        
    }       
    name = 'discourseTopicSpider'
    
    # TODO start_urls as parameter
    start_urls = ["https://community.openenergymonitor.org/top/all.json"]
    topic_fields_blacklist = [
        'post_stream',
        'timeline_lookup',
        'tags',
        'actions_summary',
        'accepted_answer',
        'details'
    ]
    
    def parse(self, response):
        j = json.loads(response.text)
        
        #print(j)

        for t in j["topic_list"]["topics"]:
            #print(t)
            url = self.baseUrl + "/t/" + str(t["id"]) + ".json"
            print(url)
            yield scrapy.Request(url, callback=self.enrich, meta={'topic': t})
            
        #print(j["topic_list"]["more_topics_url"])
            
        if "more_topics_url" in j["topic_list"].keys():
            url = j["topic_list"]["more_topics_url"]
            url = self.baseUrl + url
            url = url.replace("?",".json?")
            print(url)
            yield scrapy.Request(url, callback=self.parse)
            
    def enrich(self, response):
        topic = response.meta["topic"]
        t = json.loads(response.text)
        t_sel = {k:v for k,v in t.items() if k not in self.topic_fields_blacklist}
        
        result = {**topic, **t_sel, **{
            'created_by_user_id': t['details']['created_by']['id'],
            'created_by_username': t['details']['created_by']['username']
        }}
        
        if 'accepted_answer' in t.keys():
            result['accepted_answer_post_id'] = t['accepted_answer']['post_number']
            result['accepted_answer_username'] = t['accepted_answer']['username']
        
        yield result

"""

#TODO integrate this into DiscourseCommunityFactory.scrape_data()

topics = pd.read_json("oem_topics_details2.jl", lines=True)
posts = pd.read_json("oem_posts_2.jl", lines=True)

a_pc = posts.drop_duplicates(subset=["id"]).topic_id.value_counts().to_dict()
b_pc = topics.drop_duplicates(subset=["id"]).groupby(by="id").posts_count.mean().to_dict()
missing = {k:v-a_pc[k] for k,v in b_pc.items() if k in a_pc.keys() and v-a_pc[k]>0}
missing_topics_ids = list(missing.keys())

"""

class DiscoursePostsSpider(scrapy.Spider):
    
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 0.25,
        'AUTOTHROTTLE_MAX_DELAY': 0.5,
        'DOWNLOAD_DELAY': 0.25,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1        
    }       
    name = 'discoursePostsSpider'
    
    # TODO
    start_urls = []
    #["https://community.openenergymonitor.org/t/{}.json".format(tid)
    #              for tid in topics.id.tolist() if tid in missing_topics_ids]

    post_fields_blacklist = [
        'avatar_template',
        'link_counts',
        'actions_summary'
    ]
    

    
    def parse(self, response):
        j = json.loads(response.text)
        
        for p in j["post_stream"]["posts"]:
            yield {k:v for k,v in p.items() if k not in self.post_fields_blacklist}
        
        num_posts = len(j["post_stream"]["stream"])
        for i in range(26,num_posts+6,20):
            url = f"https://community.openenergymonitor.org/t/{j['id']}/{i}.json"
            yield scrapy.Request(url, callback=self.parse_posts)
            
    def parse_posts(self, response):
        j = json.loads(response.text)
        
        for p in j["post_stream"]["posts"]:
            yield {k:v for k,v in p.items() if k not in self.post_fields_blacklist}
            
            
class DiscourseUsersSpider(scrapy.Spider):
    
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 0.25,
        'AUTOTHROTTLE_MAX_DELAY': 0.5,
        'DOWNLOAD_DELAY': 0.25,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1        
    }       
    name = 'discoursePostsSpider'
    start_urls = []
    #["https://community.openenergymonitor.org/u/{}.json".format(uname)
    #              for uname in set(posts.username) - set(users.username)]

    user_fields_blacklist = [
        'avatar_template',
        'profile_background_upload_url',
        'custom_avatar_template',
        'featured_user_badge_ids'
    ]
    
    def parse(self, response):
        j = json.loads(response.text)
        
        yield {
            **{k:v for k,v in j["user"].items() if k not in self.user_fields_blacklist},
            **{
                'badges': j["badges"] if "badges" in j.keys() else None
            },
            **{
                'country': j["user"]["user_fields"]["1"]
            }
        }            