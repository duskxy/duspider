import scrapy
from bsj.items import BsjItem
from scrapy import Request

class BsjSpider(scrapy.Spider):
    name = 'bsj'
#    allowed_domains = ['www.bishijie.com']
#    start_urls = ['http://www.bishijie.com/kuaixun/']
 
    headers = {
        "Host": "www.baishijie.com",
        "Referer": "http://www.bishijie.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0"
    }
    def start_requests(self):
        url = 'http://www.bishijie.com/kuaixun/'
        yield Request(url,headers=self.headers)
   
    def parse(self,response):
        from scrapy.shell import inspect_response
        inspect_response(response, self)
        bsjpop = response.xpath('//div[@class="kuaixun_list"]/div/ul')
         
        for i in bsjpop:
            item = BsjItme
            item['title'] = i.xpath('/li/h2/text()').extract()
            item['create_time'] = i.xpath('/span/text()').extract()
            item['content'] = i.xpath('/li/div/text()').extract()
            yield item
