import scrapy
import logging
import numpy as np
import json
import pandas as pd


class PPFriendsSpider(scrapy.Spider):
    name = 'pp_friends'
  
    def start_requests(self):
        friendpages = []
        ids = pd.read_json("members.jl", lines=True)['id'].tolist()
        for i in ids:
            meta = {
                'id': i
            }
            url = 'https://davehakkens.nl/community/members/{}/friends/'.format(i)
            friendpages.append(scrapy.Request(url, callback=self.parse, meta=meta))

        return friendpages    

    def parse(self, response):
        next_page  = response.css("#member-dir-pag-bottom > a.next.page-numbers::attr(href)").get()
        id = response.meta['id']
        #print(response.xpath('//*[@id="members-list"]//a/@href').getall())
        friends = set([l.replace("https://davehakkens.nl/community/members/","").replace("/profile/","").replace("/","") for l in response.xpath('//*[@id="members-list"]//a/@href').getall()])
        yield {
            'id': id,
            'friends': ",".join(friends)
        }
        if next_page is not None:
            yield response.follow(next_page, self.parse, meta=response.meta)