# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class tiebaItem(scrapy.Item):
    # define the fields for your item here like:
    # 图片链接
    url = scrapy.Field()
    # 帖子标题，作为文件夹名存储本帖子的图片
    title = scrapy.Field()

