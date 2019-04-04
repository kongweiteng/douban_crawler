# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from .es_model import Field
from elasticsearch_dsl.connections import connections

es = connections.create_connection(hosts=['127.0.0.1'])


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


# 将建立的字段进行分词处理
# *args 元组 **args字典
def conduct_suggest(index, *args):
    """
    :param index: 操作的数据库
    :param args: 需要进行分词的内容
    :return: 返回分词之后的列表
    """
    # 声明空集合
    use_words = set()
    # 声明列表
    suggest = []
    # 分词的分重
    for text, weight in args:
        # 调用分词接口
        words = es.indices.analyze(
            index=index,
            params={
                'filter': ['lowercase']
            },
            body={
                'analyzer': 'ik_max_word',
                'text': text
            }
        )
        analyzer_word = set([x['token'] for x in words['tokens']])
        print(analyzer_word)
        # 计算差集
        new_words = analyzer_word - use_words
        # 加入suggest之前,这条数据在suggest是不存在的
        suggest.append({'input': list(new_words), 'weight': weight})
        use_words = analyzer_word
    # suggest是没有重复数据的
    # [{'input':['土豆','豆','逆','袭'],'weight':10},{'words':['天蚕'],'weight':8}]
    return suggest


class ZiroomItem(scrapy.Item):
    # 自如类型（合租、整租...）
    ziroom_type = scrapy.Field()
    # 地铁线路
    subway_line = scrapy.Field()
    # 地铁站点
    subway_station = scrapy.Field()
    # 房间title
    room_title = scrapy.Field()
    # 距离地铁站距离
    subway_distance = scrapy.Field()
    # 房间编号
    room_number = scrapy.Field()
    # 描述（独卫）
    room_describe = scrapy.Field()
    # 价格
    room_price = scrapy.Field()
    # 房间详情链接
    room_link = scrapy.Field()
    # 房间面积
    room_acreage = scrapy.Field()
    # 户型
    house_type = scrapy.Field()
    # 房间楼层
    room_floor = scrapy.Field()
    # 时间
    room_time = scrapy.Field()
    pass

    # 将数据保存到es搜索服务器中
    def save_es(self):
        novel = Field()
        # 从传递进来的item中取值
        novel.subway_line = self['subway_line']
        novel.subway_station = self['subway_station']
        novel.room_title = self['room_title']
        novel.subway_distance = self['subway_distance']
        novel.room_number = self['room_number']
        novel.room_describe = self['room_describe']
        novel.room_price = self['room_price']
        novel.room_link = self['room_link']
        novel.room_acreage = self['room_acreage']
        novel.house_type = self['house_type']
        novel.room_floor = self['room_floor']
        novel.room_time = self['room_time']
        # 将数据对应分词信息进行保存
        # 将某些字段进行分词处理, 将处理后的数据保存到suggest中
        # novel.suggest = conduct_suggest('novels', (novel.room_describe, 10), (novel.author, 8))
        novel.save()
