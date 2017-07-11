# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# 保存所爬取数据的容器，扩展了scrapy的Item类
class AutohomeItem(scrapy.Item):
    size = scrapy.Field()
    name = scrapy.Field()
    detail = scrapy.Field()
    score = scrapy.Field()
