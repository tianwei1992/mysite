"""
一个发送邮件的API。

调用方式：POST+参数
参数有4个：subject message from_email to_emial,除message外不能为空
返回是json：例如{'code':0,'message':'邮件发送成功.'}，code为0表示成功发送，其他则为异常

2019.03.26
"""

import logging
logger = logging.getLogger('mysite.mailapi.info')

from django.http import JsonResponse
# Create your views here.
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from utils.get_client_infos import get_visitor_ip
from utils.get_ip_infos import get_location_calling_free_api

#先禁用防跨站请求伪造功能，方便 curl post 测试和调用
@csrf_exempt
@require_POST
def send_email(request):
    return_data = {'code':0,'message':'邮件发送成功.'}

    subject = request.POST.get('subject', '')
    message = request.POST.get('message', '')
    from_email = request.POST.get('from_email', '')
    to_email = request.POST.get('to_email', '')

    #设置 from_email 的默认值
    if not message:
        message = ''   # 内容留空是允许的吧？


    print("subject",subject)
    print("message",message)
    print("from_email",from_email)

    if subject and to_email and from_email:
        try:
            to_email = to_email.split(';') #多个收件人以;分隔
            print("to_email",to_email)
            send_mail(subject, message, from_email, to_email)
        except BadHeaderError:
            return_data['code'] = 1
            return_data['message'] = '邮件发送失败.'
    else:
        # In reality we'd use a form class
        # to get proper validation errors.
        return_data['code'] = 0
        return_data['message'] = '检查必要字段是否完整'

    ip = get_visitor_ip(request)
    ip_infos = get_location_calling_free_api(ip)
    logger.info(f"ip = {ip}, subject = {subject },message = {message }, from_email = {from_email }, to_email = {to_email }, return_data = {return_data }")
    return JsonResponse(return_data)
