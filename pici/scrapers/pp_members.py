import scrapy
import logging
import numpy as np


class PPMemberSpider(scrapy.Spider):
    name = 'pp_members'
    start_urls = ['https://davehakkens.nl/community/members/'] + ['https://davehakkens.nl/community/members/?upage={}'.format(p) for p in range(2,1013)]

    def parse(self, response):
        for member in response.css('#members-list li div.membercard a'):
            yield response.follow(member, callback=self.parse_member)
            
    def parse_member(self, response):
        data_fields = {
            'age': np.nan,
            'years_member': np.nan,
            'name': '',
            'topics': '',
            'dedication': np.nan
        }
        
        data = [d.strip() for d in response.css('#item-body > div.profile > div.bp-widget.base div.data p::text').getall()]
        ded = response.css('#item-body > div.profile > div.profilesidebar > div > div.mycred > div > div::text').get().replace(" ","")
        
        data_fields['name'] = data[0]
        
        for d in data[3:]:
            if "years" in d and not 'http' in d:
                try:
                    data_fields['age'] = int(d.replace(" years",""))
                except ValueError:
                    pass
            elif "year member" in d and not "http" in d:
                try:
                    data_fields['years_member'] = int(d.replace(" year member","").replace(" ",""))
                except ValueError:
                    pass
            elif "," in d and not "http" in d:
                data_fields['topics'] = d     
                
        try:
            data_fields['dedication'] = int(ded)
        except ValueError:
            pass
        
        friends = scrapy.Request(response.url + 'friends/', callback=self.parse_friends)
        friendlist = ",".join(friends) if isinstance(friends, list) else ""
        print(friends)

        
        yield {**{
            'id': response.css('#item-header-content > h2.user-nicename::text').get().strip().replace("@",""),
            'name': response.xpath('//*[@id="item-header-content"]/div[1]/text()').get(),
            'location': response.css('#item-header-content > div.header-location::text').get(),
            'links': ";".join([d.strip() for d in response.css('#item-body > div.profile > div.bp-widget.base div.data a::attr(href)').getall()]),
            'badges': ",".join([b.strip() for b in response.xpath('//*[@id="mycred-users-badges"]/div/img/@alt').getall()])
        },**data_fields}
        
        
    def parse_friends(self, response):
        print("hello friends! 0000000000000000000000000000000000000000000000000")
        friends = [l.replace("https://davehakkens.nl/community/members/","").replace("/profile/") for l in response.css("div.membercard > a::attr(href)").getall()]
        next_page  = response.css("#member-dir-pag-bottom > a.next.page-numbers::attr(href)").get()        
        next_friends = scrapy.Request(next_page, callback=self.parse_friends)

        yield friends + next_friends
            