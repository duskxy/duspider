# -*- coding: utf-8 -*-
import scrapy
from bishijie.items import FreebufItem
from scrapy.loader import ItemLoader

import sys

class FbfSpider(scrapy.Spider):
    name = 'fbf'
    allowed_domains = ['www.freebuf.com']
    custom_settings = {
        "COOKIES_ENABLED": False
    }
    def start_requests(self):
        headers = {
            'Host': 'www.freebuf.com',
            'Referer': 'http://www.freebuf.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
         }
        for url in range(1,37):
            yield scrapy.Request("http://www.freebuf.com/page/{}".format(url),headers=headers,callback=self.parse)
    def parse(self, response):
        all_url = response.xpath('//div[@class="news-img"]/a/@href').extract()
        print(all_url)
        if not all_url:
            if 'acw_sc__v3' in response.body.decode("utf-8"):
                print("错误,请重试")
                sys.exit()
        # print(title)

    def parse_fbf():
        pass
