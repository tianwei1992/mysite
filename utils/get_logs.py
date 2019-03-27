import sys, os
import datetime
cur_dir = os.path.dirname(os.path.abspath(__file__))
proj_dir = os.path.dirname(cur_dir)
log_dir = os.path.join(proj_dir, 'logs')

sys.path.append(log_dir)

def get_date():
    today=datetime.date.today() #'2018-01-01'
    return str(today)


def get_logs_today(file_name):
    content = ''
    today = get_date()

    file_path = os.path.join(log_dir, file_name)
    with open (file_path, 'r') as f:
        for line in f.readlines():
            if today in line:
                content += line
    return content
   


if __name__ == "__main__":
    file_name = 'article_infos.log'
    content = get_logs_today(file_name) 
    print(content)
