import douban.getToken
import base64
import urllib
import urllib.request
from PIL import Image
import pytesseract
'''
通用物体和场景识别
'''


def parsePng(img):
    # text = pytesseract.image_to_string(Image.open(img), lang='chi_sim')
    # print(text)
    # im = Image.open(img)
    # out = im.resize((45, 45), Image.ANTIALIAS)  # resize image with high-quality
    # out.save(img)
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general"
    # 二进制方式打开图片文件
    f = open(img, 'rb')
    img = base64.b64encode(f.read())

    params = {"image": img}
    params = urllib.parse.urlencode(params).encode('utf-8')
    access_token = eval(douban.getToken.getToken())['access_token']
    request_url = request_url + "?access_token=" + access_token
    request = urllib.request.Request(url=request_url, data=params)
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    response = urllib.request.urlopen(request)
    content = response.read()
    if (content):
        print
        content


if __name__ == "__main__":
    parsePng('20190311181153410.png')
