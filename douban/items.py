# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 序号
    serial_number = scrapy.Field()
    # 电影名称
    movie_name = scrapy.Field()
    # 电影的介绍
    introduce = scrapy.Field()
    # 星级
    star = scrapy.Field()
    # 电影的评论数
    evaluate = scrapy.Field()
    # 电影的描述
    describe = scrapy.Field()

    pass


class ZiroomItem(scrapy.Item):
    # 自如类型（合租、整租...）
    ziroom_type = scrapy.Field()
    # 地铁线路
    subway_number = scrapy.Field()
    # 房间title
    room_title = scrapy.Field()
    # 距离地铁站距离
    subway_distance = scrapy.Field()
    # 描述（独卫）
    room_describe = scrapy.Field()
    # 价格
    room_price = scrapy.Field()
    # 房间详情链接
    room_link = scrapy.Field()
    # 房间面积
    room_acreage = scrapy.Field()
    # 房间类型（两室一厅）
    room_type = scrapy.Field()
    # 房间楼层
    room_floor = scrapy.Field()
    pass
