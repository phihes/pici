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
            auth_url = topic.css('div.topic-desc > p > span.bbp-topic-started-by > a.bbp-author-name::attr(href)').get()
            forum_url = topic.css('div.topic-desc > p span.bbp-topic-started-in a::attr(href)').get()
            
            t = {
                'id': url.split("/")[-2],
                #'url': url,
                'title': topic.css('div.topic-desc > a::text').get(),
                'author': auth_url.split("/")[-2] if auth_url is not None else np.nan,
                'forum_url': forum_url if forum_url is not None else np.nan,
                'forum': topic.css('div.topic-desc > p > span.bbp-topic-started-in > a::text').get(),
                'num_replies': int(topic.css('li.bbp-topic-reply-count::text').get()),
                #'replies': replies
            }
            if url:
                yield scrapy.Request(url, callback=self.parse_first_post, meta={'topic': t})
    
    """
    def parse_replies(self, response):

        topic = response.meta['topic']
        next_page  = response.css(".bbp-pagination-links > a.next.page-numbers::attr(href)").get()

        for reply in response.css('div.topic-reply'):
            author = ''
            date = ''
            likes = 0                
            try:
                author = reply.css('div.author a.').get().split("/")[-2]
            except:
                pass
            try:
                date = reply.css('div.replyheader > div.reply-date::text')
            except:
                pass
            try:
                likes = int(reply.css('span.count-box::text'))
            except:
                pass
            text = reply.xpath('string(//div[@class="content"])').extract()

            topic['replies'].append({
                'author': author,
                'date': date,
                'likes': likes,
                'text': text
            })

        if next_page:
            yield scrapy.Request(next_page, callback=self.parse_replies, meta={'topic': topic})
        else:
            yield topic
        """
        
        
    def parse_first_post(self, response):
        
        topic = response.meta['topic']
        
        post = response.css('div.topic-lead')
        
        topic['date'] = post.css('div.author > div.date::text').get().strip()
        topic['text'] = post.xpath('string(//div[@class="content"])').extract()[0]
        
        
        counters = post.css('div.actions > div.topicounter')
        num_subs = 0
        num_favs = 0
        num_likes = 0
        
        subs = counters.css('div.dav_topic_subscriber > span::text').get()
        likes = counters.css('div.dav_topic_like > span::text').get()
        favs = counters.css('div.dav_topic_favorit > span::text').get()
        
        try:
            num_subs = int(subs.replace("subscribers","").strip()) if subs is not None else 0
        except:
            pass       
        try:
            num_favs = int(favs.replace("saved","").strip()) if favs is not None else 0
        except:
            pass
        
        try:
            num_likes = int(likes.replace("likes","").strip()) if likes is not None else 0
        except:
            pass
        
        topic['num_subs'] = num_subs
        topic['num_favs'] = num_favs
        topic['num_likes'] = num_likes
        
        yield topic
        
        #if topic['num_replies'] > 0:
        #    yield scrapy.Request(response.request.url, callback=self.parse_replies, meta={'topic': topic})
            
        
 