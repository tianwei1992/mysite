"""调用send_mail API"""
import os, sys
from req import get_res

proj_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
settings_dir = os.path.join(proj_dir, 'mysite')

sys.path.append(settings_dir)


from get_envs import if_online_env


if if_online_env():
    http_port = '10025'
else:
    http_port = '10024'

def send_a_email(subject, message, to_email, from_email='tianweigrace@qq.com'):
    url_api = f"http://localhost:{http_port}/api/sendemail/"
    request_method = "post"
    form_data = {
    'subject': subject,
    'message': message, 
    'to_email': to_email, 
    'from_email': from_email
}
    res_json  = get_res(url_api, request_method, form_data=form_data)
    return res_json


if __name__ == "__main__":
    subject = "测试主体"
    message = "测试内容"
    to_email =  "tianweigrace@qq.com"
    res = send_a_email(subject, message, to_email)
    print(res)





