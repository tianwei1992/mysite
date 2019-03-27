import sys, os
import schedule
import time

proj_dir = os.path.dirname(os.path.abspath(__file__))
utils_dir = os.path.join(proj_dir, "utils")
sys.path.append(utils_dir)


from get_logs import get_logs_today
from send_emails import send_a_email

def send_logs_today():
    file_name = 'article_infos.log'
    subject = "[今天的日志]来自lovelyhouse"
    to_email =  "tianweigrace@qq.com"
    message = get_logs_today(file_name)
    res = send_a_email(subject, message, to_email)
    


schedule.every().day.at("22:50").do(send_logs_today)

while True:
    schedule.run_pending()
    time.sleep(1)
