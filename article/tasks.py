from __future__ import absolute_import, unicode_literals

import json
import logging
import time

from celery import shared_task
from utils.get_client_infos import get_visitor_ip, get_useragent
from utils.get_ip_infos import get_location_calling_free_api


info_logger = logging.getLogger('mysite.article.info')
"""
def mul(x, y):
    info_logger.info("in")
    time.sleep(10)
    info_logger.info("out")
    return x * y
"""


@shared_task
def start_logging(log_str, ip=None, username=None, ua=None, **kwargs):
    """填充模板log_str，生成日志内容，并写入文件"""
    if ip:
        ip_infos = get_location_calling_free_api(ip)
        log_str += 'IP:{}[{}] '.format(ip, ip_infos)
    if ua:
        log_str += 'UA:{} '.format(ua)
    if username:
        log_str += 'Visitor:{} '.format(username)
    if kwargs:
        str_list = [ k+':'+v for k,v in kwargs.items()]
        log_str += ' '.join(str_list)
    # 测试是否异步
    # time.sleep(5)
    log_str += '\n'
    info_logger.info(log_str)
    
