import urllib, urllib.request, sys
import ssl


# client_id 为官网获取的AK， client_secret 为官网获取的SK
def getToken():
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=gNilXoYt1EYIm5vqqArzvATL&client_secret=5NfQMAbSQzGvLn67G7MG2BGRI5OOobbk'
    request = urllib.request.Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urllib.request.urlopen(request)
    content = response.read()
    if (content):
        return content
