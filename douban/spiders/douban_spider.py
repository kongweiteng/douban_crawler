# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem


class DoubanSpiderSpider(scrapy.Spider):
    # 爬虫的名字
    name = 'douban_spider'
    # 允许的域名
    allowed_domains = ['movie.douban.com']
    # 入口url，
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        # print(response.text)
        movie_list = response.xpath("//div[@class='article']//ol[@class='grid_view']//li")
        for i_item in movie_list:
            douban_item = DoubanItem()
            douban_item['serial_number'] = i_item.xpath(".//div[@class='item']//em/text()").extract_first()
            douban_item['movie_name'] = i_item.xpath(
                ".//div[@class='info']//div[@class='hd']/a/span[1]/text()").extract_first()
            content = i_item.xpath(".//div[@class='info']//div[@class='bd']/p[1]/text()").extract()
            for i_content in content:
                content_s = ''.join(i_content.split())
                douban_item['introduce'] = content_s
            douban_item['star'] = i_item.xpath(".//div[@class='star']/span[@class='rating_num']/text()").extract_first()
            douban_item['evaluate'] = i_item.xpath(".//div[@class='star']/span[4]/text()").extract_first()
            douban_item['describe'] = i_item.xpath(".//div[@class='bd']/p[@class='quote']/span/text()").extract_first()
            print(douban_item)
