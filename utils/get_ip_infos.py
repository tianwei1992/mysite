"""
Update: 2019.03.15 
从IP获得IP相关信息
"""


import re
import logging
import requests
import time
from lxml import etree, objectify


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

    text = None
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


def parse_infos(text):
    # parser = etree.XMLParser(remove_comments = True)
    # html = objectify.parse(text, parser=parser)
    city = None
    carrier = None
    if text:
        html = etree.HTML(text)
        try:
            city = html.xpath('//table//tr[3]/td/span')[0].text
            carrier = html.xpath('//table//tr[4]/td/span')[0].text
        except:
            logger.eror("这个ip没有城市信息")
    res_dic = {"city": city, "carrier": carrier}
    return res_dic
    

def get_location_from_ip(ip_addr):
    """
    从ip地址获得周边信息，暂时包括所在城市和运营商
    请求页面：https://www.ipip.net/ip.html
    请求方法：post
    解析方法：lxml

    Params:
        ip_addr -> str ，形如1.1.1.1
    Return:
        dict ,形如 {'city': '中国香港', 'carrier': 'microsoft.com'}
"""
    url_api = "https://www.ipip.net/ip.html"
    form_data = {'ip': ip_addr}
    request_method = "post"
    headers = {
    'authority': 'www.ipip.net',
    'origin': 'https://www.ipip.net',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'referer': 'https://www.ipip.net/ip.html',
    'accept-encoding': 'gzip, deflate, br',
    'cookie': '__jsluid=d8582d8bf018a8eaad61d8bf06660398; _ga=GA1.2.941283959.1550463698; __cfduid=deae8c973f76fc2bf64245190b7cabcc51550469323; _gid=GA1.2.236318088.1552107049; LOVEAPP_SESSID=fcebab02c7185a4bc4787191541b7aa31d8b6177; Hm_lvt_123ba42b8d6d2f680c91cb43c1e2be64=1552437900,1552485555,1552569570,1552621221; Hm_lpvt_123ba42b8d6d2f680c91cb43c1e2be64=1552621244',
}
    res_text  = get_res(url_api, request_method, headers=headers, form_data=form_data)
    ip_infos = parse_infos(res_text)
    return ip_infos


def get_location_calling_free_api(ip_addr):
    """调用免费的接口
       请求http://freeapi.ipip.net/117.115.44.90
       接口返回的是长度为4的列表，形如["中国","四川","成都","","移动"]"""
    url_api = "http://freeapi.ipip.net/"+ip_addr
    request_method = "get"

    time.sleep(0.3)  # 受到接口访问频率限制，间隔0.2s以上，加大延时也可作为测试，观察在IO耗时很长很长时的异步效果 
    res_text  = get_res(url_api, request_method)

    pat = re.compile('\"(.*?)\"')
    res_list = pat.findall(res_text)
    country, province, city, town, carrier = res_list
    city = country + province + city + town

    ip_infos = {"city": city, "carrier": carrier}
    return ip_infos
    

if __name__ == "__main__":
    ip_addr = "65.52.175.85"
    # ip_infos = get_location_from_ip(ip_addr) 被封了
    ip_infos = get_location_calling_free_api(ip_addr)
    print(ip_addr, ip_infos)
