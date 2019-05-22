
from users.models import User
import datetime
from world.models import Site

def make_birthdays():
    birthday_today = datetime.date.today().strftime('%m%d')  # 当前日期


    nan = []
    nv = []
    name = []
    try:
        users = User.objects.filter(realBirthday=birthday_today)
        # TODO 要换成官方
        my_user = User.objects.get(pk=9)
        if users:
            for user in users:

                if user.gender == "男":
                    nan.append(1)
                else:
                    nv.append(0)

                name.append(user.nickname)

            nan_len = len(nan)
            nv_len = len(nv)

            all_count = nan_len + nv_len

            if nan_len and nv_len:

                content = "今天共有{}位寿星,我掐指一算,小哥哥有{}位,小姐姐有{}位.快来祝福身边的他/她吧,反正我迫不及待的想认识了！他/她们的名字分别为:{}.".format(
                    all_count, len(nan), len(nv), str(name))

            elif nan_len > 0:
                content = "今天共有{}位寿星,全是小哥哥哦,他们的名字分别为:{}.快来祝福身边的他吧,我要表白小哥哥！".format(all_count, str(name))

            elif nv_len > 0:
                content = "今天共有{}位寿星,全是小姐姐哦,他们的名字分别为:{}.快来祝福身边的她吧,我要表白小姐姐！".format(all_count, str(name))

            Site.objects.create(content=content,tag="生日祝福",Cuser=my_user)
            print(birthday_today)
    except:
        print(birthday_today+" 生日祝福出错啦")




