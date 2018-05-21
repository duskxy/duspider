# -*- coding: utf-8 -*-
import pymysql
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class BishijiePipeline(object):
    def __init__(self):
#        self.host = 'localhost'
#        self.port = 3306
#        self.user = 'root'
#        self.password = 'a05370385a'
#        self.db = 'bsj'
#        self.charset = 'utf8'
#        self.conn = pymysql.connect(self.host,self.port,self.user,self.password,self.db,self.charset)
        self.conn = pymysql.connect(host='localhost',port=3306,user='root',passwd='a05370385a',db='bsj',charset='utf8')
    def process_item(self, item, spider):
        cursor = self.conn.cursor()
        sql = 'insert into bsj(title,create_time,content) values(%s,%s,%s)'
        cursor.execute(sql,(item['title'],item['create_time'],item['content']))
        self.conn.commit()
        return item