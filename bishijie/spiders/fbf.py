# -*- coding: utf-8 -*-
import scrapy
from bishijie.items import FreebufItem,FreebufItemLoader
from scrapy.loader import ItemLoader

import sys

class FbfSpider(scrapy.Spider):
    name = 'fbf'
    allowed_domains = ['www.freebuf.com']
    custom_settings = {
        "COOKIES_ENABLED": False,
        'ITEM_PIPELINES': {
            'bishijie.pipelines.FreebufPipeline':300,
 
    },
    }
    def start_requests(self):
        headers = {
            'Host': 'www.freebuf.com',
            'Referer': 'http://www.freebuf.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
         }
        for url in range(1,853):
        #for url in range(1,2):
            yield scrapy.Request("http://www.freebuf.com/page/{}".format(url),headers=headers,callback=self.parse)
    def parse(self, response):
        all_url = response.xpath('//div[@class="news-img"]/a/@href').extract()
        for rurl in all_url:
            yield scrapy.Request(rurl,callback=self.parse_fbf)
    def parse_fbf(self,response):
        freebuf_item = FreebufItem()
        item_loader = FreebufItemLoader(item=FreebufItem(),response=response)
        item_loader.add_css("ftitle",".articlecontent .title h2::text")
        item_loader.add_css("fcontent","#contenttxt *::text")
        item_loader.add_css("publish_time",".articlecontent .time::text")
        item_loader.add_value("url",response.url)
        freebuf_item = item_loader.load_item()
        yield freebuf_item
