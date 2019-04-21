# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymongo
from taobao_s.search_text import KEY_WORDS


class TaobaoSPipeline(object):

    def open_spider(self,spider):
        # client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        # db = client['taobao']
        # self.q = db[spider.settings['KEY_WORDS']]
        self.file = open(KEY_WORDS+'.json', 'w', encoding='utf8')

    def process_item(self, item, spider):
        content = json.dumps(dict(item),ensure_ascii=False) + '\n'
        self.file.write(content)
        # self.q.update({'nid': item['nid']}, {'$set': dict(item)}, True)
        return item

    def close_spider(self,spider):
        self.file.close()
