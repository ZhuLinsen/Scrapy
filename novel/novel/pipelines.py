# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

class NovelPipeline(object):
    def process_item(self, item, spider):
        cur_path = os.getcwd()
        file_path = cur_path + os.path.sep + item['name']
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        file_name = file_path + os.path.sep + item['title'] + '.txt'
        with open(file_name, 'a', encoding='utf-8') as f:
            f.write(item['title']+'\n'+'-'*50+'\n')
            for i in item['content']:
                    f.write(i.replace(u'\xa0', ' ')+'\n')
            f.write('\n')
        return item
