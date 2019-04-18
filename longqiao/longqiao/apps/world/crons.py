
from users.models import User
import datetime


def make_birthdays():
    birthday_today = datetime.date.today().strftime('%m%d')  # 当前日期
    print(birthday_today)

    nan = []
    nv = []
    name = []
    try:
        users = User.objects.filter(realBirthday=birthday_today)
        if users:
            for user in users:
                print(user.gender)
                if user.gender == "男":
                    nan.append(1)
                else:
                    nv.append(0)
                print(user.username)
                name.append(user.username)

            nan_len = len(nan)
            nv_len = len(nv)

            all_count = nan_len + nv_len

            if nan_len and nv_len:

                print("今天共有{}位寿星,我掐指一算,小哥哥有{}位,小姐姐有{}位.快来祝福身边的他/她吧,简简单单的一句生日祝福,却可以带来无限的感动和幸福！他/她们的名字分别为:{}.".format(
                    all_count, len(nan), len(nv), str(name)))

            elif nan_len > 0:
                print("今天共有{}位寿星,全是小哥哥哦,他们的名字分别为:{}.快来祝福身边的他吧,简简单单的一句生日祝福,却可以带来无限的感动和幸福！".format(all_count, str(name)))

            elif nv_len > 0:
                print("今天共有{}位寿星,全是小姐姐哦,他们的名字分别为:{}.快来祝福身边的她吧,简简单单的一句生日祝福,却可以带来无限的感动和幸福！".format(all_count, str(name)))
    except:
        raise Exception("生日祝福出错啦")


