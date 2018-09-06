# -*- coding: utf-8 -*-
import scrapy
from bishijie.items import FreebufItem
from scrapy.loader import ItemLoader


class FbfSpider(scrapy.Spider):
    name = 'fbf'
    allowed_domains = ['www.freebuf.com']
    DOWNLOAD_DELAY = 1
    custom_settings = {
        "COOKIES_ENABLED": True
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
        title = response.css('.news-info')
        print(all_url)
        # print(title)

    def parse_fbf():
        pass
