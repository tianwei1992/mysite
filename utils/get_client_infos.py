"""从HttpReques获得客户端信息，包括IP、UA"""
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
from get_ip_infos import get_location_calling_free_api

def get_visitor_ip(request):
    if request.META.get('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    return ip


def get_useragent(request):
    ua = request.META['HTTP_USER_AGENT']
    return ua


def get_visitor_infos(request):
    ip = get_visitor_ip(request)
    ip_infos = get_location_calling_free_api(ip)
    ua = get_useragent(request)

    client_infos = ip, ip_infos, ua
    return client_infos


