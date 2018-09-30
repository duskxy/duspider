# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
import scrapy


class FreebufItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

class BishijieItem(scrapy.Item):
    title = scrapy.Field()
    create_time = scrapy.Field()
    content = scrapy.Field()
    crawl_time = scrapy.Field()

class FreebufItem(scrapy.Item):
    ftitle = scrapy.Field()
    fcontent = scrapy.Field()
    publish_time = scrapy.Field()
    url = scrapy.Field()
    crawl_time = scrapy.Field()
