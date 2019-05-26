
import os
import sys
import django
from channels.routing import get_default_application

# # application加入查找路径中
# app_path = os.path.abspath(os.path.join(
#     os.path.dirname(os.path.abspath(__file__)), os.pardir))
# sys.path.append(os.path.join(app_path, 'zanhu'))  # ../zanhu/zanhu

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# 添加导包路径
import sys
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# TODO 线上环境要修改
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "longqiao.settings.dev")
django.setup()
application = get_default_application()
