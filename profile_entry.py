# -*- coding: utf-8 -*-
"""
使用 [line_profiler](https://github.com/rkern/line_profiler) 时不能接收命令行参数，需要以一个独立的脚本运行

# 在需要进行性能测试的函数上添加装饰器 @profile
# 然后运行
kernprof -l -v profile_entry.py
"""

import os
import sys

import django
from django.core.management import call_command
from django.conf import settings

sys.path.append(os.path.dirname(os.path.realpath(__file__)))  # 把 manage.py所在目录添加到系统目录
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings' # 设置setting文件
# settings.configure() do not do this
django.setup()


def test_brand():
    # python manage.py test course.tests.BrandTest.test_details -k --settings mysite.settings
    #call_command("test", "course.tests.BrandTest.test_details", "-k")  # , verbosity=3, interactive=False)
    call_command("test", "course.tests.BrandTest.test_details")  # , verbosity=3, interactive=False)


if __name__ == '__main__':
    test_brand()
