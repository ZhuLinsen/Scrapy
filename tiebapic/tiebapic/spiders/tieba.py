# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from tiebapic.items import tiebaItem
import re

class TiebaSpider(Spider):
    name = 'tieba'
    allowed_domains = ['tieba.baidu.com']
    start_url = ['http://tieba.baidu.com/']

    keyword = '壁纸'
    start_url = 'https://tieba.baidu.com/f?kw={keyword}'
    tiezi_url = 'https://tieba.baidu.com{pp}'

    def start_requests(self):

        yield Request(url=self.start_url.format(keyword=self.keyword), callback=self.url_parse)

    def url_parse(self, response):
        #results = response.css('a::attr(href)').extract()
        results = response.css(".threadlist_lz.clearfix a::attr(href)").extract()
        urls = re.findall(r'[/]p[/]\d{10}', str(results))
        for i in urls:
            yield Request(url=self.tiezi_url.format(pp=i), callback=self.image_parse)

    def image_parse(self, response):
        item = tiebaItem()
        item['url'] = response.css('.BDE_Image::attr(src)').extract()
        item['title'] = response.css('h3::attr(title)').extract_first()
        yield item

