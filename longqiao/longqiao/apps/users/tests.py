from django.test import TestCase
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "longqiao.settings.dev")
django.setup()
from users.models import User
# from django.contrib.auth.models import User
# Create your tests here.
from users import constants
if __name__ == '__main__':

    from fdfs_client.client import Fdfs_client

    client = Fdfs_client(constants.FDFS)
    ret = client.upload_by_filename('/home/python/Desktop/timg.jpg')
    print(ret)
    #
    # import random
    # gen = ['男','女']
    # # User.objects.filter()
    # d =['信息工程系','会计系','法学系','外语系','艺术系']
    # c =['电子商务1601','信息管理1601','计算机科学与技术1601']
    #
    # q=['01','02','03','04','05','06','07','08','09','10','11','12']
    # w = [str(i) for i in range(10,31)]
    #
    # for i in range(60000,610000):    # 创建用户
    #     user = User.objects.create_user(
    #         StudentID='%s'%i,
    #         password="avdd%s"%i,
    #         username='hello%s'%i,
    #         gender=random.choice(gen),
    #         nickname='nickname%s'%i,
    #         enrollmentDate=20160708,
    #         birthday="20{}{}".format(random.choice(q),random.choice(w)),
    #         realBirthday = "{}{}".format(random.choice(q),random.choice(w)),
    #         department=random.choice(d),
    #         sclass=random.choice(c),
    #         classes='2016',
    #         is_active=True
    #     )

    # from django_redis import get_redis_connection
    #
    # conn = get_redis_connection("default")
    # print(conn)
    #
    # from django.core.cache import cache  # 引入缓存模块
    #
    # cache.set('v', '555', 60 * 60)  # 写入key为v，值为555的缓存，有效期30分钟
    #
    # print(cache.has_key('v'))  # 判断key为v是否存在
    # print(cache.get('v'))  # 获取key为v的缓存
    # nan=[]
    # nv = []
    # User.objects.filter(birthday='0318')
    # name = []
    # users = User.objects.filter(birthday='0318')
    # for user in users:
    #     print(user.gender)
    #     if user.gender=="男":
    #         nan.append(1)
    #     else:
    #         nv.append(0)
    #     print(user.username)
    #     name.append(user.username)
    #     print(user.sclass)
    # print(users)
    #
    # print("小哥哥有{}位，小姐姐有{}位,他/她们的名字分别为:{}".format(len(nan),len(nv),str(name)))
    import datetime
    def make_birthdays():
        birthday_today = datetime.date.today().strftime('%m%d') # 当前日期
        print(birthday_today)


        nan = []
        nv = []
        name = []
        try:
            users = User.objects.filter(realBirthday=birthday_today)
            if users:
                for user in users:
                    print(user.gender)
                    if user.gender=="男":
                        nan.append(1)
                    else:
                        nv.append(0)
                    print(user.username)
                    name.append(user.username)


                nan_len = len(nan)
                nv_len = len(nv)

                all_count = nan_len+nv_len

                if nan_len and nv_len:


                    print("今天共有{}位寿星,我掐指一算,小哥哥有{}位,小姐姐有{}位.快来祝福身边的他/她吧,简简单单的一句生日祝福,却可以带来无限的感动和幸福！他/她们的名字分别为:{}.".format(all_count,len(nan), len(nv), str(name)))

                elif nan_len>0:
                    print("今天共有{}位寿星,全是小哥哥哦,他们的名字分别为:{}.快来祝福身边的他吧,简简单单的一句生日祝福,却可以带来无限的感动和幸福！".format(all_count, str(name)))

                elif nv_len>0:
                    print("今天共有{}位寿星,全是小姐姐哦,他们的名字分别为:{}.快来祝福身边的她吧,简简单单的一句生日祝福,却可以带来无限的感动和幸福！".format(all_count, str(name)))
        except:
            raise Exception("生日祝福出错啦")
    make_birthdays()