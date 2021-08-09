import scrapy
import logging
import numpy as np
import json
from urllib.parse import urlparse


# run with
# -a baseUrl=http://.../categories
class OSMSpider(scrapy.Spider):
    
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 0.1,
        'AUTOTHROTTLE_MAX_DELAY': 0.5,
        'DOWNLOAD_DELAY': 0.1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 5        
    }       
    name = 'OSMSpider'
    start_urls = ["https://forum.openstreetmap.org/"]
    
    def parse(self, response):
        for f in response.css('h3>a'):
            forum = {
                "forum_url": f.css('::attr(href)').get(),
                "forum_title": f.css('::text').get(),
                "forum_id": f.css('::attr(href)').get().split("=")[1]     
            }
            
            if forum['forum_url']:
                yield response.follow(forum['forum_url'], callback=self.parse_forum, meta=forum)
            
    def parse_forum(self, response):
        for t in response.css('td.tcl a'):
            topic = {
                "topic_title": t.css('::text').get(),
                "topic_url": t.css('::attr(href)').get(),
                "topic_id": t.css('::attr(href)').get().split("=")[1]
            }
            
            if topic['topic_url']:
                yield response.follow(topic['topic_url'], callback=self.parse_topic, meta={**response.meta, **topic})
        
        # pagination
        next_page = response.css('a[rel="next"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_forum, meta=response.meta)
            
            
    def parse_topic(self, response):
        for r in response.css('div[class~=blockpost]'):
            auth = r.css('div[class~=postleft] dl dd *::text').getall()
            id = r.css('::attr(id)').get()
            reply = {
                "reply_id": id,
                "reply_date": r.css('h2 a::text').get(),
                "reply_number": r.css('h2 span::text').get()[1:],
                "reply_content": response.xpath('string(//div[@id="' + id + '"]//div[@class="postmsg"])').extract()[0],
                "author_name": r.css('div[class~=postleft] dl dt *::text').get(),
                "author_type": r.css('div[class~=postleft] dd[class~=usertitle] *::text').get(),
                "author_from": "",
                "author_registered_date": ""
            }
            
            attr_types = {
                'author_registered_date': "Registered: ",
                'author_from': "From: "
            }
            
            for attr in auth:
                for k, a_t in attr_types.items():
                    a = attr.strip()
                    if a.startswith(a_t):
                        reply[k] = a.replace(a_t, "")
            
            yield {**reply, **response.meta}
        
        # pagination
        next_page = response.css('a[rel="next"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse_topic, meta=response.meta)        