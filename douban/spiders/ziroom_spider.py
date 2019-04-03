# -*- coding: utf-8 -*-
import re
import requests as req
from PIL import Image
import numpy as np
from io import BytesIO
import re
import scrapy
import time
from urllib.request import urlretrieve
from douban import getNumbers
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
                yield scrapy.Request("http:" + subway_station_url, callback=self.parseRoomList,
                                     meta={"subway_station_item_name": subway_station_item_name})

    # 处理每个地铁站翻页后的数据
    def parseRoomList(self, response):
        # ff = webdriver.Firefox()
        # ff.get(response.url)
        # li = ff.find_elements_by_xpath('//*[@id="houseList"]/li[1]/div[3]/p[1]/span[2]')
        subway_station_item_name = response.meta['subway_station_item_name']
        ziroom_list = response.xpath("//div[@class='t_newlistbox']//ul[@id='houseList']//li[@class='clearfix']")
        count = 0
        for room_item in ziroom_list:
            ziroom = ZiroomItem()
            ziroom['ziroom_type'] = '友家合租'
            ziroom['subway_station'] = subway_station_item_name
            ziroom['room_title'] = room_item.xpath("./div[@class='txt']/h3/a/text()").extract_first()
            ziroom['subway_distance'] = room_item.xpath(
                "./div[@class='txt']/div[@class='detail']/p[2]/span/text()").extract_first()
            room_info_rul = "http:" + room_item.xpath("./div/a/@href").extract_first()
            # 处理房间的价格
            # print(response.text)
            img_url = self.get_img_url(response.text)[0]
            offerset = self.get_img_url(response.text)[1][count]
            img_number = self.get_num_list(img_url)
            # 根据图片的数据和offerset 计算价格
            price = ''
            for offerset_item in offerset:
                price = price + str(img_number[offerset_item])
            count += 1
            ziroom['room_price'] = int(price)
            # 交给处理房间详情的方法
            yield scrapy.Request(room_info_rul, callback=self.parseRoomInfo,
                                 meta={"ziroom": ziroom})
            # print(room_info_rul)
            # print(dict(ziroom))

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
    def parseRoomInfo(self, response):
        ziroom = response.meta['ziroom']
        # 房间连接详情
        ziroom['room_link'] = response.url
        # 房屋编号
        ziroom['room_number'] = response.xpath("//div[@class='aboutRoom gray-6']/h3/text()").extract()[1].strip()
        # 房屋描述
        ziroom['room_describe'] = response.xpath("//div[@class='aboutRoom gray-6']/p/text()").extract_first()
        # 房屋面积
        ziroom['room_acreage'] = "".join(
            response.xpath("//ul[@class='detail_room']/li[1]/text()").extract_first().split())
        # 户型
        ziroom['house_type'] = "".join(
            response.xpath("//ul[@class='detail_room']/li[3]/text()").extract_first().split())
        # 楼层
        ziroom['room_floor'] = "".join(
            response.xpath("//ul[@class='detail_room']/li[4]/text()").extract_first().split())
        ziroom['room_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(ziroom)

    def get_img_url(self, str):
        priceImage = re.compile('var ROOM_PRICE = (.*?);').search(str).group(1)
        priceImage = eval(priceImage)
        imageUrl = 'http:' + priceImage['image']
        imageOffset = priceImage['offset']
        return imageUrl, imageOffset

    def get_price(html, str):
        priceImage = re.compile('var ROOM_PRICE = (.*?);').search(str).group(1)
        priceImage = eval(priceImage)
        imageUrl = 'http:' + priceImage['image']
        imageOffset = priceImage['offset']
        imageFile = html.get_picture(imageUrl)
        # print(imageFile)
        numbers = getNumbers.getNum(imageFile)
        # print(imageOffset)
        # print(numbers)
        return numbers, imageOffset

    def get_picture(image_url, imageUrl):
        """ 获取图片 """
        picture_name = 'ziroom.png'
        urlretrieve(url=imageUrl, filename=picture_name)
        return picture_name

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
