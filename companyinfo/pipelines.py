# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json

from companyinfo.spiders.shuidiinfo import DateEncoder


class CompanyinfoPipeline(object):
    def __init__(self):
        self.f = codecs.open('全部信息.json', 'a+', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False, cls=DateEncoder) + '\n'
        self.f.write(line)
        return item

    def close_spider(self, spider):
        self.f.close()
