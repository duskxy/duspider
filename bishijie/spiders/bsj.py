# -*- coding: utf-8 -*-
import scrapy
import sys
from bishijie.items import BishijieItem


class BsjSpider(scrapy.Spider):
    name = 'bsj'
    allowed_domains = ['http://www.bishijie.com/kuaixun/']
    start_urls = ['http://www.bishijie.com/kuaixun/']

    def parse(self, response):
        Bsj = BishijieItem()
        kx = response.xpath('//div[@class="kuaixun_list"]/div/ul')
        for bitem in kx:
            Bsj['title'] = bitem.xpath('li/h2/text()').extract()[0]
            Bsj['create_time'] = bitem.xpath('span/text()').extract()[0]
            Bsj['content'] = bitem.xpath('li/div/text()').extract()[0].replace('\r\n','')
            yield Bsj
            
