import scrapy
import logging
import numpy as np
import json
from urllib.parse import urlparse
import pandas as pd

topics = pd.read_json("oem_topics_details2.jl", lines=True)
posts = pd.read_json("oem_posts_2.jl", lines=True)

a_pc = posts.drop_duplicates(subset=["id"]).topic_id.value_counts().to_dict()
b_pc = topics.drop_duplicates(subset=["id"]).groupby(by="id").posts_count.mean().to_dict()
missing = {k:v-a_pc[k] for k,v in b_pc.items() if k in a_pc.keys() and v-a_pc[k]>0}
missing_topics_ids = list(missing.keys())


class DiscoursePostsSpider(scrapy.Spider):
    
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 0.25,
        'AUTOTHROTTLE_MAX_DELAY': 0.5,
        'DOWNLOAD_DELAY': 0.25,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1        
    }       
    name = 'discoursePostsSpider'
    start_urls = ["https://community.openenergymonitor.org/t/{}.json".format(tid)
                  for tid in topics.id.tolist() if tid in missing_topics_ids]

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
            url = "https://community.openenergymonitor.org/t/{}/{}.json".format(
                j["id"], i)
            yield scrapy.Request(url, callback=self.parse_posts)
            
    def parse_posts(self, response):
        j = json.loads(response.text)
        
        for p in j["post_stream"]["posts"]:
            yield {k:v for k,v in p.items() if k not in self.post_fields_blacklist}