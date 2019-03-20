import logging

from celery_tasks.main import celery_app
from bs4 import BeautifulSoup

logger = logging.getLogger("django")

from django_redis import get_redis_connection
import json

@celery_app.task(name='getCourse')
def getCourse(text):

    soup = BeautifulSoup(text, 'html.parser')
    # self.__set__VIEWSTATE(soup)
    print("课程：            ")

    # 获取课表，kburl是课表页面url,为什么有个Referer参数,这个参数代表你是从哪里来的。就是登录后的主界面参数。这个一定要有。

    content = soup.find('table', id='Table6')

    banji = soup.select('option[selected="selected"]')[-1].get_text()



    lesson = []
    list = []
    for tr in content.find_all('tr')[2:10:2]:
        for td in tr.find_all('td'):
            print(td.get_text())
            # if td.get_text()==" ":
            #     list.append("空")
            if td.get_text() not in ["上午", '下午']:
                list.append(td.get_text())

        lesson.append(list)
        list = []

    redis_conn = get_redis_connection('courses')

    redis_conn.set("%s" % banji,str(lesson)) # 设置字符串　键是班级，值是课程

    # return