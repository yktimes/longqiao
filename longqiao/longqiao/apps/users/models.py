from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    """用户模型类"""
    StudentID = models.BigIntegerField(verbose_name='学号',unique=True)

    avatar =   models.CharField(max_length=200, verbose_name="用户头像",default="http://47.94.253.97:8888/group1/M00/00/00/rBGjLFyhvy2Aaue5AAAOobGPP50788.jpg")

    nickname = models.CharField(max_length=60,verbose_name='昵称',db_index=True)
    gender = models.CharField(max_length=10,verbose_name='性别')
    enrollmentDate = models.CharField(max_length=30,verbose_name='入学日期')
    birthday = models.CharField(max_length=30,verbose_name='出生日期')

    realBirthday = models.CharField(max_length=20, verbose_name='生日',db_index=True)
    department= models.CharField(max_length=30,verbose_name='系别')
    sclass = models.CharField(max_length=50,verbose_name='班级')
    classes = models.CharField(max_length=20,verbose_name='级别')
    mobile = models.CharField(max_length=11, null=True, verbose_name='手机号')

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name