import scrapy
import logging
import numpy as np
import json
from urllib.parse import urlparse


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