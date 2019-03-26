"""
Update: 2019.03.26 
发送http请求，获得响应
"""
import logging
import requests
import time


logger = logging.getLogger('mysite.error')
DEFAULT_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
DEFAULT_HEADERS =  {
    'user-agent': DEFAULT_UA, 
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
}

def get_res(url, request_method, form_data=None, headers=DEFAULT_HEADERS):
    if request_method == "get":
        res = requests.get(url, headers=headers)
    elif request_method == "post":
        res = requests.post(url, headers=headers, data=form_data)

    text = ''
    try:
        res.raise_for_status()
        res.encoding = res.apparent_encoding
        text = res.text
    except Exception as e:
        res.encoding = res.apparent_encoding
        logger.error(res.text)
        logger.error(e)
        logger.error("请求失败,爬虫被封掉了？")
    return text



if __name__ == "__main__":
    ip = "65.52.175.85"
    url_api = "http://freeapi.ipip.net/"+ip
    request_method = "get"
    res_text  = get_res(url_api, request_method)
    print(res_text)

