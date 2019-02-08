# -*- coding: utf-8 -*-
import scrapy
import re
from novel.items import NovelItem

class NovelsSpider(scrapy.Spider):
    name = 'novels'
    allowed_domains = ['www.zwdu.com']
    start_urls = ['https://www.zwdu.com/book/23925/']

    def parse(self, response):
        ulist = response.css('#list a::attr(href)').extract()
        for i in ulist:
            url = 'https://www.zwdu.com'+i
            yield scrapy.Request(url = url, callback = self.parse_text)

    def parse_text(self, response):
        item = NovelItem()
        item['name'] = response.css('title::text').extract_first().split(' ')[0]
        item['title'] = response.css('h1::text').extract_first()
        item['content'] = response.css('#content::text').extract()
        yield item




