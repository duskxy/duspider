# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BishijieItem(scrapy.Item):
    title = scrapy.Field()
    create_time = scrapy.Field()
    content = scrapy.Field()
    crawl_time = scrapy.Field()

class FreebufItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    publish_time = scrapy.Field()
    url = scrapy.Field()
    crawl_time = scrapy.Field()
