# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem
from utils.config import Redis,myconn


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BishijiePipeline(object):
#    def __init__(self):
#        self.conn = pymysql.connect(host='localhost',port=3306,user='',passwd='',db='',charset='')
    def process_item(self, item, spider):
        cursor = myconn.cursor()
        sql = 'insert into bsj(title,create_time,content) values(%s,%s,%s)'
        cursor.execute(sql,(item['title'],item['create_time'],item['content']))
        myconn.commit()
        return item
class DuplicatesPipeline(object):
#    def __init__(self):
#        self.Redis = redis.StrictRedis(host='127.0.0.1',password='',port=6379,db=0)
    def process_item(self,item,spider):
        if Redis.exists('title:{}'.format(item['title'])):
            raise DropItem("Duplicate item found: {}".format(item))
        else:
            Redis.set('title:{}'.format(item['title']),1)
            Redis.expire('title:{}'.format(item['title']),86400)
            return item
