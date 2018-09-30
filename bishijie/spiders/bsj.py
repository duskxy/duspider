# -*- coding: utf-8 -*-
import scrapy
import sys
from bishijie.items import BishijieItem


class BsjSpider(scrapy.Spider):
    name = 'bsj'
    allowed_domains = ['www.bishijie.com']
    start_urls = ['http://www.bishijie.com/kuaixun/']
    
    custom_settings = {
        'ITEM_PIPELINES': {
               'bishijie.pipelines.DuplicatesPipeline': 200,
               'bishijie.pipelines.BishijiePipeline': 300,

        },

 
    }

    def parse(self, response):
        Bsj = BishijieItem()
        kx = response.xpath('//div[@class="kuaixun_list"]/div/ul')
        for bitem in kx:
            Bsj['title'] = bitem.xpath('li/h2/a/text()').extract()[0]
            Bsj['create_time'] = bitem.xpath('span/text()').extract()[0]
            Bsj['content'] = bitem.xpath('li/div/a/text()').extract()[0].replace('\r\n','').replace(' ','')
            yield Bsj
            
