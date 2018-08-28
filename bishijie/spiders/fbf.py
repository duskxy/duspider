# -*- coding: utf-8 -*-
import scrapy
from bishijie.items import FreebufItem
from scrapy.contrib.loader import ItemLoader


class FbfSpider(scrapy.Spider):
    name = 'fbf'
    allowed_domains = ['www.freebuf.com']
    start_urls = ['http://www.freebuf.com/page/1']
    headers = {
        'Host': 'www.freebuf.com',
        'Referer': 'http://www.freebuf.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
    }
    custom_settings = {
        "COOKIES_ENABLED": True
    }
    def parse(self, response):
        all_url = response.xpath('//div[@class="news-img"]/a/@href').extract()
        title = response.css('.news-info')
        print(all_url)
        # print(title)

    def parse_fbf():
        pass
