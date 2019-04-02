# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from douban.settings import mongo_host, mongo_port, mongo_db_name, mongo_db_douban_table, mongo_user, mongo_password, \
    mongo_db_ziroom_table


class DoubanPipeline(object):
    def __init__(self):
        host = mongo_host
        port = mongo_port
        user = mongo_user
        password = mongo_password
        dbname = mongo_db_name
        douban_table_name = mongo_db_douban_table
        ziroom_table_name = mongo_db_ziroom_table
        client = pymongo.MongoClient('mongodb://{0}:{1}@{2}:{3}'.format(user, password, host, port))
        mydb = client[dbname]
        self.ziroom_post = mydb[ziroom_table_name]
        self.douban_post = mydb[douban_table_name]

    def process_item(self, item, spider):
        if spider.name == 'douban_spider':
            data = dict(item)
            self.douban_post.insert(data)
        if spider.name == 'ziroom_spider':
            data = dict(item)
            self.ziroom_post.insert(data)
        return item
