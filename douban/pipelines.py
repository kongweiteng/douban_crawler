# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from .es_save import save
from openpyxl import Workbook
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

        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(
            ['自如类型', '地铁线路', '地铁站点', '房间title', '距离地铁站距离', '房间编号', '描述', '价格', '房间详情链接', '房间面积', '户型', '房间楼层',
             '时间'])  # 设置表头

    def process_item(self, item, spider):
        if spider.name == 'douban_spider':
            data = dict(item)
            self.douban_post.insert(data)
        if spider.name == 'ziroom_spider':
            data = dict(item)
            self.ziroom_post.insert(data)
            if 'ziroom_type' in item:
                ziroom_type = item['ziroom_type']
            else:
                ziroom_type = None

            if 'subway_line' in item:
                subway_line = item['subway_line']
            else:
                subway_line = None

            if 'subway_station' in item:
                subway_station = item['subway_station']
            else:
                subway_station = None

            if 'room_title' in item:
                room_title = item['room_title']
            else:
                room_title = None

            if 'subway_distance' in item:
                subway_distance = item['subway_distance']
            else:
                subway_distance = None

            if 'room_number' in item:
                room_number = item['room_number']
            else:
                room_number = None

            if 'room_describe' in item:
                room_describe = item['room_describe']
            else:
                room_describe = None

            if 'room_price' in item:
                room_price = item['room_price']
            else:
                room_price = None

            if 'room_link' in item:
                room_link = item['room_link']
            else:
                room_link = None

            if 'room_acreage' in item:
                room_acreage = item['room_acreage']
            else:
                room_acreage = None

            if 'house_type' in item:
                house_type = item['house_type']
            else:
                house_type = None
            if 'room_floor' in item:
                room_floor = item['room_floor']
            else:
                room_floor = None

            if 'room_time' in item:
                room_time = item['room_time']
            else:
                room_time = None
            line = [ziroom_type, subway_line, subway_station, room_title, subway_distance, room_number, room_describe,
                    room_price, room_link, room_acreage, house_type, room_floor, room_time]  # 把数据中每一项整理出来
            # if line:
            # self.ws.append(line)  # 将数据以行的形式添加到xlsx中
            # self.wb.save('E:/source/python/douban/excel/ziroom.xlsx')  # 保存xlsx文件
        return item


# 将爬虫爬取的数据存储搜索服务器中
class EsPipline(object):
    def __init__(self):
        self.index = 'ziroom'
        self.doc_type = 'ziroom'

    def process_item(self, item, spider):
        save(self.index, self.doc_type, item)
        return item
