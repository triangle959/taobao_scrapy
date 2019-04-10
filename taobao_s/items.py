# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TaobaoSItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    price = scrapy.Field()
    sales = scrapy.Field()
    title = scrapy.Field()
    nick = scrapy.Field()
    loc = scrapy.Field()
    detail_url = scrapy.Field()
    nid = scrapy.Field()
    sellerid = scrapy.Field()

# class TmallItem(scrapy.item):
#     total = scrapy.Field()
#     rateContent = scrapy.Field()
#     rateDate = scrapy.Field()
#     auctionSku = scrapy.Field()
#     content = scrapy.Field()
#     contentDate = scrapy.Field()
