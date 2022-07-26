from pici.helpers import create_graph
import pandas as pd
import scrapy
from scrapyscript import Job, Processor
import logging
import numpy as np
import json
from urllib.parse import urlparse
from pici import helpers, Community, CommunityFactory


class OSMCommunity(Community):
    name = "OpenStreetMap"
    date_column = "date"
    contributor_column = "author_name"
    topic_column = "topic_id"
    text_column = "reply_content"

    DEFAULT_ATTRIBUTES = {
        "yesterday": "2021-07-11",
        "today": "2021-07-12",
        "node_data": [
            'author_from',
            'author_type',
            'author_registered_date',
            'forum_title',
            'topic_title'
        ],
        "original_date_column": "reply_date"
    }

    def _set_data(self, data, start, end):

        d = {}

        if 'posts' in data.keys():
            if isinstance(data['posts'], pd.DataFrame):

                p = data['posts']

                # fix paging issue
                p["topic_id"] = p["topic_id"].apply(lambda x: x.split("&")[0])

                # prepare date column in post data
                p["date"] = pd.to_datetime(
                    p[self._attr["original_date_column"]]
                        .str.replace("Yesterday", self._attr["yesterday"])
                        .str.replace("Today", self._attr["today"])
                )

                # set time slice
                d['posts'] = self.timeslice(p, self.date_column, start, end)

                # set node data (contributor-level)
                d['contributors'] = d['posts'].groupby(
                    by=self.contributor_column)[
                    self._attr["node_data"]].agg(helpers.series_most_common)  # pd.Series.mode)

                d['topics'] = d['posts'][['topic_id', 'topic_title',
                                          'topic_url', 'forum_title',
                                          'forum_id', 'forum_url']].drop_duplicates()
                d['topics'] = d['topics'].set_index('topic_id')
                # .groupby(by=self.topic_column).agg('count')

            else:
                raise TypeError("posts are not a pandas dataframe")
        else:
            raise ValueError("posts are missing in data")

        self._data = d
        self._posts = d['posts']
        self._contributors = d['contributors']
        self._topics = d['topics']

    def _generate_graph(self):
        return create_graph(
            self.posts,
            self.contributors,
            self.contributor_column,
            self.topic_column,
            self.contributors.columns
        )


class OSMCommunityFactory(CommunityFactory):
    name = "osm"
    cache_data = ['posts']

    def _create_community(self, name, start, end):
        return OSMCommunity(name, self._data, start, end)

    def scrape_data(self):
        processor = Processor(settings=None)
        posts = pd.DataFrame(processor.run(Job(OSMSpider)))
        self._data = {
            'posts': posts
        }
        self.add_data_to_cache({
            'posts': posts
        })


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
