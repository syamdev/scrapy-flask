# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CraigslistItem(scrapy.Item):
    url = scrapy.Field()
    date = scrapy.Field()
    title = scrapy.Field()
    address = scrapy.Field()
    #description = scrapy.Field()
    compensation = scrapy.Field()
    employment_type = scrapy.Field()
