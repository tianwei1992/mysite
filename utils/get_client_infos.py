def get_visitor_ip(request):
    if request.META.get('HTTP_X_FORWARDED_FOR'):
        ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    return ip

def get_useragent(request):
    ua = request.META['HTTP_USER_AGENT']
    return ua

