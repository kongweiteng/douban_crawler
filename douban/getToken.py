import urllib, urllib.request, sys
import ssl


# client_id 为官网获取的AK， client_secret 为官网获取的SK
def getToken():
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=YtGlGktDVEN373LMVtGBZQFZ&client_secret=CDEn5vBbtUXxt4M0uWfzcSryNZll7oeY'
    request = urllib.request.Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urllib.request.urlopen(request)
    content = response.read()
    if (content):
        return content
