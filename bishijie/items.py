# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose,TakeFirst,Join
import scrapy

def frvau(value):
    return str(value)
def rekg(value):
    return value.strip().replace('\n','').replace('\r','').replace(' ','')

class FreebufItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

class BishijieItem(scrapy.Item):
    title = scrapy.Field()
    create_time = scrapy.Field()
    content = scrapy.Field()
    crawl_time = scrapy.Field()

class FreebufItem(scrapy.Item):
    ftitle = scrapy.Field(
        input_processor = MapCompose(rekg)
    )
    fcontent = scrapy.Field(
        input_processor = MapCompose(frvau,rekg),
        output_processor = Join("")
    )
    publish_time = scrapy.Field()
    url = scrapy.Field()
    crawl_time = scrapy.Field()
