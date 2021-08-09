import scrapy
import logging
import numpy as np
import json
from urllib.parse import urlparse
import pandas as pd

posts = pd.read_json("oem_posts_2.jl", lines=True)
users = pd.read_json("oem_users.jl", lines=True)

class DiscourseUsersSpider(scrapy.Spider):
    
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 0.25,
        'AUTOTHROTTLE_MAX_DELAY': 0.5,
        'DOWNLOAD_DELAY': 0.25,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1        
    }       
    name = 'discoursePostsSpider'
    start_urls = ["https://community.openenergymonitor.org/u/{}.json".format(uname)
                  for uname in set(posts.username) - set(users.username)]

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