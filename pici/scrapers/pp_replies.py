import scrapy
import logging
import numpy as np
from bs4 import BeautifulSoup

class PPTopicSpider(scrapy.Spider):
    name = 'pp_topics'
    start_urls = ['https://davehakkens.nl/topics/page/{}/'.format(p) for p in range(1,302)]

    def parse(self, response):
        for topic in response.css('#bbp-forum-0 li.bbp-body ul'):
            url = topic.css('div.topic-desc > a::attr(href)').get()
            if url:
                yield scrapy.Request(url, callback=self.parse_replies, meta={'tid': url.split("/")[-2]})

    def parse_replies(self, response):
        
        tid = response.meta['tid']

        next_page  = response.css(".bbp-pagination-links > a.next.page-numbers::attr(href)").get()

        for reply in response.css('div.topic-reply'):
            author = ''
            date = ''
            likes = 0                
            try:
                author = reply.css('div.author a::attr(href)').get().split("/")[-2]
            except:
                pass
            try:
                date = reply.css('div.replyheader > div.reply-date::text').get().strip()
            except:
                pass
            try:
                likes = int(reply.css('span.count-box::text').get())
            except:
                pass
            text = reply.xpath('string(//div[@class="content"])').extract()[0]

            yield {
                'topic': tid,
                'author': author,
                'date': date,
                'likes': likes,
                'text': text
            }

            if next_page:
                yield scrapy.Request(next_page, callback=self.parse_replies, meta={'tid': tid})