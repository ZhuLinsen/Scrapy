# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from tiebapic.items import tiebaItem
import re

class TiebaSpider(Spider):
    name = 'tieba'
    allowed_domains = ['tieba.baidu.com']
    start_url = ['http://tieba.baidu.com/']

    #改变keyword可获取任意贴吧的图片
    keyword = '壁纸'
    start_url = 'https://tieba.baidu.com/f?kw={keyword}&pn={page}'
    tiezi_url = 'https://tieba.baidu.com{pp}'

    '''
    构造壁纸吧前两千个页面的请求
    具体的贴吧吧可查看是否有2000个页面
    '''
    def start_requests(self):
        for i in range(2000):
            yield Request(url=self.start_url.format(keyword=self.keyword, page=str(i*50)), callback=self.url_parse)

    '''
    解析页面的帖子链接，并且发起请求获取帖子的数据
    调用image_parse函数解析帖子页面，获取所有图片链接
    '''
    def url_parse(self, response):
        results = response.css(".threadlist_lz.clearfix a::attr(href)").extract()
        urls = re.findall(r'[/]p[/]\d{10}', str(results))
        for i in urls:
            yield Request(url=self.tiezi_url.format(pp=i), callback=self.image_parse)

    '''
    获取本帖子的标题和图片url存入item，
    获取当前页数和尾页页数，如果不是尾页则爬取下一页
    '''
    def image_parse(self, response):
        url_page = response.url[0:37]
        item = tiebaItem()
        item['url'] = response.css('.BDE_Image::attr(src)').extract()
        item['title'] = response.css('h3::attr(title)').extract_first()
        cur_page = response.css('.l_pager.pager_theme_4.pb_list_pager span::text').extract_first()
        last_page = response.css('.l_posts_num .l_reply_num span::text').extract()[1]
        yield item

        if cur_page and last_page and int(cur_page) < int(last_page):
            next_url = url_page + '?pn={page}'.format(page=str(int(cur_page)+1))
            yield Request(url=next_url, callback=self.image_parse)



