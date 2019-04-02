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

    def parse(self, response):
        print(response.text)
