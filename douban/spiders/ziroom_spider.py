# -*- coding: utf-8 -*-
import re
import time
import numpy as np
import requests as req
import scrapy
from PIL import Image
from io import BytesIO
from douban.items import ZiroomItem


class ZiroomSpiderSpider(scrapy.Spider):
    # 爬虫的名字
    name = 'ziroom_spider'
    # 允许的域名
    allowed_domains = ['ziroom.com']
    # 入口url，
    start_urls = ['http://www.ziroom.com/z/nl/z2-o2.html']
    # 爬虫爬取页数控制初始值
    page_count = 1
    # 爬虫爬取页数 10为只爬取一页
    page_end = 1

    # 处理地铁线路以及地铁站点的循环
    def parse(self, response):
        subway_line_list = response.xpath('//*[@id="selection"]/div/div/dl[3]/dd/ul/li/span')
        for subway_line_item in subway_line_list:
            subway_station_list = subway_line_item.xpath('./following-sibling::div[1]/span/a')
            subway_line = subway_line_item.xpath('./a/text()').extract_first()

            # print(list)
            # subway_station_list = response.xpath("//div[@class='selection_con']//dl[3]//dd/ul/li/div/span[@class='tag']/a")
            for subway_station_item in subway_station_list:
                subway_station_item_name = subway_station_item.xpath("./text()").extract_first()
                if subway_station_item_name:
                    if subway_station_item_name != '全部':
                        subway_station_url = subway_station_item.xpath("./@href").extract_first()
                        yield scrapy.Request("http:" + subway_station_url, callback=self.parseRoomList,
                                             meta={"subway_station_item_name": subway_station_item_name,
                                                   "subway_line": subway_line})

    # 处理每个地铁站翻页后的数据
    def parseRoomList(self, response):
        # print(response.request.headers['User-Agent'])
        if response.status == 200:
            subway_station_item_name = response.meta['subway_station_item_name']
            subway_line = response.meta['subway_line']
            ziroom_list = response.xpath("//div[@class='t_newlistbox']//ul[@id='houseList']//li[@class='clearfix']")
            img_info = self.get_img_url(response.text)
            img_url = img_info[0]
            offerset = img_info[1]
            img_number = self.get_num_list(img_url)
            count = 0
            for room_item in ziroom_list:
                ziroom = ZiroomItem()
                ziroom['ziroom_type'] = '友家合租'
                ziroom['subway_station'] = subway_station_item_name
                ziroom['subway_line'] = subway_line
                ziroom['room_title'] = room_item.xpath("./div[@class='txt']/h3/a/text()").extract_first()
                ziroom['subway_distance'] = room_item.xpath(
                    "./div[@class='txt']/div[@class='detail']/p[2]/span/text()").extract_first()
                room_info_rul = "http:" + room_item.xpath("./div/a/@href").extract_first()
                # 根据图片的数据和offerset 计算价格
                price = ''
                for offerset_item in offerset[count]:
                    price = price + str(img_number[offerset_item])
                count += 1
                ziroom['room_price'] = int(price)
                # page = response.xpath("//a[@class='active']/text()").extract_first()
                # print({"lin": subway_line, "sub": subway_station_item_name, "page": page, })
                # 交给处理房间详情的方法
                yield scrapy.Request(room_info_rul, callback=self.parseRoomInfo,
                                     meta={"ziroom": ziroom})
            next_link = response.xpath('//*[@id="page"]/a[@class="next"]/@href').extract()
            if next_link != 'javascript:;':
                if next_link:
                    next_link = next_link[0]
                    if next_link is not None:
                        yield scrapy.Request("http:" + next_link, callback=self.parseRoomList,
                                             meta={"subway_station_item_name": subway_station_item_name,
                                                   "subway_line": subway_line})
                else:
                    # 爬虫结束
                    return None

    def parseRoomInfo(self, response):
        ziroom = response.meta['ziroom']
        # 房间连接详情
        ziroom['room_link'] = response.url
        # 房屋编号
        room_number = response.xpath("//div[@class='aboutRoom gray-6']/h3/text()").extract()
        if room_number:
            ziroom['room_number'] = room_number[1].strip()
        # 房屋描述
        room_describe = response.xpath("//div[@class='aboutRoom gray-6']/p/text()").extract_first()
        if room_describe:
            ziroom['room_describe'] = "".join(room_describe.split())
        # 房屋面积
        room_acreage = response.xpath("//ul[@class='detail_room']/li[1]/text()").extract_first()
        if room_acreage:
            ziroom['room_acreage'] = "".join(room_acreage.split())
        # 户型
        house_type = response.xpath("//ul[@class='detail_room']/li[3]/text()").extract_first()
        if house_type:
            ziroom['house_type'] = "".join(house_type.split())
        # 楼层
        room_floor = response.xpath("//ul[@class='detail_room']/li[4]/text()").extract_first()
        if room_floor:
            ziroom['room_floor'] = "".join(room_floor.split())
        ziroom['room_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # print(ziroom)
        yield ziroom

    def get_img_url(self, str):
        priceImage = re.compile('var ROOM_PRICE = (.*?);').search(str).group(1)
        priceImage = eval(priceImage)
        imageOffset = ''
        imageUrl = 'http:' + priceImage['image']

        if "offset" in priceImage:
            imageOffset = priceImage['offset']
        return imageUrl, imageOffset

    def read_image_url(self, img_url):
        response = req.get(img_url)
        im = Image.open(BytesIO(response.content)).convert('RGB')
        data = np.array(im)
        return data

    def read_image(self, imageName):
        im = Image.open(imageName).convert('RGB')
        data = np.array(im)
        return data

    def get_num(self, n):
        l_num = []
        m = 0
        x = n
        while True:
            if m < 9:
                x0, x1, = np.split(x, [30], axis=1)
                # print(x0)
                # plt.imshow(x0)
                # plt.pause(0.001)
                # print(x1)
                # plt.imshow(x1)
                # plt.pause(0.001)
                l_num.append(x0)
                x = x1
                m += 1
                continue
            else:
                l_num.append(x)
                # plt.imshow(x)
                # plt.pause(0.001)
                break
        return l_num

    def get_0_9(self):
        l_num = self.get_num(self.read_image('20190311181153410.png'))
        x2, x4, x3, x6, x8, x5, x1, x9, x0, x7 = l_num
        list_num = [x0, x1, x2, x3, x4, x5, x6, x7, x8, x9]
        return list_num

    def get_num_list(self, png):
        l = []
        list_num = self.get_0_9()
        l_num_test = self.get_num(self.read_image_url(png))
        for i in range(0, 10):
            # plt.imshow(l_num_test[i])
            # plt.pause(0.001)
            for w in range(0, 10):
                # print((i == w).all())
                if (l_num_test[i] == list_num[w]).all():
                    # plt.imshow(w)
                    # plt.pause(0.001)
                    l.append(w)
                    # print(w)
                    break
        # print (l)
        return l
