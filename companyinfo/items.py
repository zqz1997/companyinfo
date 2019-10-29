# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CompanyinfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    company_list = scrapy.Field()
    name = scrapy.Field()
    metaModel = scrapy.Field()
    source = scrapy.Field()
    url = scrapy.Field()
    header = scrapy.Field()
    get = scrapy.Field()
    date = scrapy.Field()
    content = scrapy.Field()
