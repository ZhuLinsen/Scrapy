# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request


class TiebapicPipeline(object):
    def process_item(self, item, spider):
        return item

class ImagesPipeline(ImagesPipeline):

    '''
    获取item的ulr，生成Request请求，加入队列，等待下载,
    同时通过request.meta携带文件夹名
    '''
    def get_media_requests(self, item, info):
        for i in item['url']:
            yield Request(i, meta={'item': item})

    '''
    处理每张照片，返回当下request对象路径和文件名
    '''
    def file_path(self, request, response=None, info=None):
        url = request.url
        file_name = url.split('/')[-1]
        title = request.meta['item']['title']
        path = title+'/'+file_name
        return path

    '''
    单个item完成下载处理，通过判断文件路径是否存在，不存在说明下载失败，剔除下载失败的图片  
    '''
    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]
        if not image_path:
            raise DropItem('Item contains no images')
        #item['image_paths'] = image_path
        return item
