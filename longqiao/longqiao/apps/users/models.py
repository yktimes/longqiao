from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    """用户模型类"""
    StudentID = models.BigIntegerField(verbose_name='学号', unique=True)

    avatar = models.CharField(max_length=200, verbose_name="用户头像",
                              default="http://47.94.253.97:8888/group1/M00/00/00/rBGjLFyhvy2Aaue5AAAOobGPP50788.jpg")

    nickname = models.CharField(max_length=60, verbose_name='昵称', db_index=True)
    gender = models.CharField(max_length=10, verbose_name='性别')
    enrollmentDate = models.CharField(max_length=30, verbose_name='入学日期')
    birthday = models.CharField(max_length=30, verbose_name='出生日期')

    sign = models.CharField(max_length=150, verbose_name='个人签名')
    is_site = models.BooleanField(default=False,verbose_name="是否有权限开通首页")
    realBirthday = models.CharField(max_length=20, verbose_name='生日', db_index=True)
    department = models.CharField(max_length=30, verbose_name='系别')
    sclass = models.CharField(max_length=50, verbose_name='班级')
    classes = models.CharField(max_length=20, verbose_name='级别')
    mobile = models.CharField(max_length=11, null=True, verbose_name='手机号')

    def __str__(self):
        return self.nickname

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name



class FriendShip(models.Model):
    """
    关注关系表

    """
    followed = models.ForeignKey(User, related_name='followed',on_delete=models.CASCADE)  # 被别人关注

    follower = models.ForeignKey(User, related_name='follower',on_delete=models.CASCADE)  # 关注别人
    date = models.DateTimeField(auto_now_add=True)



    class Meta:
        ordering = ('-date',)


    def __str__(self):
        return f'{self.follower} follow {self.followed}'

    @staticmethod
    def follow(from_user, to_user):
        FriendShip(follower=from_user,
                   followed=to_user).save()  # 关注

    @staticmethod
    def unfollow(from_user, to_user):
        f = FriendShip.objects.filter(follower=from_user, followed=to_user).all()
        print(f)
        if f:
            f.delete()  # 取关

    @staticmethod
    def user_followed(from_user):
        followeders = FriendShip.objects.filter(follower=from_user).all()
        print("fff", followeders)
        user_followed = []
        for followeder in followeders:
            user_followed.append(followeder.followed)
        return user_followed  # 得到from_user关注的人，返回列表

    @staticmethod
    def user_follower(from_user):
        followeders = FriendShip.objects.filter(followed=from_user).all()
        user_followed = []
        for followeder in followeders:
            user_followed.append(followeder.follower)
        return user_followed  # 得到关注我的人，返回列表
