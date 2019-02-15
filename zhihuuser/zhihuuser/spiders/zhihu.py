# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Spider, Request

from zhihuuser.items import UserItem


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['zhihu.com']
    start_urls = ['http://zhihu.com/']

    start_token = 'yin-jiao-shou-32'

    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include=allow_message%2Cis_followed%2Cis_following%2Cis_org%2Cis_blocking%2Cemployments%2Canswer_count%2Cfollower_count%2Carticles_count%2Cgender%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics'

    follow_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset={offset}&limit=20'

    follower_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset={offset}&limit=20'

    def start_requests(self):

        yield Request(url=self.user_url.format(user=self.start_token), callback=self.user_parse)
        yield Request(url=self.follow_url.format(user=self.start_token, offset=0), callback=self.follow_parse)
        yield Request(url=self.follower_url.format(user=self.start_token, offset=0), callback=self.follower_parse)

    def user_parse(self, response):
        results = json.loads(response.text)
        item = UserItem()
        for field in item.fields:
            if field in results.keys():
                item[field] = results.get(field)
        yield item

        yield Request(url=self.follow_url.format(user=results.get('url_token'), offset=0), callback=self.follow_parse)
        yield Request(url=self.follower_url.format(user=results.get('url_token'), offset=0),
                      callback=self.follower_parse)

    def follow_parse(self, response):
        results = json.loads(response.text)

        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(url=self.user_url.format(user=result.get('url_token')), callback=self.user_parse)

        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next_page = results.get('paging').get('next')
            yield Request(url=next_page, callback=self.follow_parse)

    def follower_parse(self, response):
        results = json.loads(response.text)

        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(url=self.user_url.format(user=result.get('url_token')), callback=self.user_parse)

        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next_page = results.get('paging').get('next')
            yield Request(url=next_page, callback=self.follower_parse)
