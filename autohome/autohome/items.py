# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AutohomeItem(scrapy.Item):
    car_name = scrapy.Field()
    car_club_url = scrapy.Field()