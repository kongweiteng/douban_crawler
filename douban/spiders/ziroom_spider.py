# -*- coding: utf-8 -*-
import scrapy
from douban.items import ZiroomItem


class ZiroomSpiderSpider(scrapy.Spider):
    # 爬虫的名字
    name = 'ziroom_spider'
    # 允许的域名
    allowed_domains = ['ziroom.com']
    # 入口url，
    start_urls = ['http://www.ziroom.com/z/nl/z2-o2.html']

    # 处理地铁站的循环
    def parse(self, response):
        subway_station_list = response.xpath("//div[@class='selection_con']//dl[3]//dd/ul/li/div/span[@class='tag']/a")
        for subway_station_item in subway_station_list:
            subway_station_item_name = subway_station_item.xpath("./text()").extract_first()
            if subway_station_item_name != '全部':
                subway_station_url = subway_station_item.xpath("./@href").extract_first()
                yield scrapy.Request("http:" + subway_station_url, callback=self.parseRoom,
                                     meta={"subway_station_item_name": subway_station_item_name})

    # 处理每个地铁站翻页后的数据
    def parseRoom(self, response):
        subway_station_item_name = response.meta['subway_station_item_name']
        ziroom_list = response.xpath("//div[@class='t_newlistbox']//ul[@id='houseList']//li[@class='clearfix']")
        for room_item in ziroom_list:
            ziroom = ZiroomItem()
            ziroom['ziroom_type'] = '友家合租'
            ziroom['subway_station'] = subway_station_item_name

    # ziroom = ZiroomItem()
    # ziroom["subway_station"] = subway_station_item_name

    # print(nih)

    # ziroom_list = response.xpath("//div[@class='t_newlistbox']//ul[@id='houseList']//li")
    # for room_item in ziroom_list:
    #     ziroom = ZiroomItem()
    #
    #     ziroom['ziroom_type'] = '友家合租'
    #     ziroom['subway_number'] = room_item.xpath("")
    #     if subway_station_name_list != '全部':
    #         for subway_station_name_item in subway_station_name_list:
    #             ziroom = ZiroomItem()
    #             ziroom['subway_station'] = subway_station_name_item
    #             print(ziroom)
