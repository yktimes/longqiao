from django.db import models
from longqiao.utils.models import BaseModel
# Create your models here.


class ConfessionWall(models.Model):
    """
    表白墙
    """

    content = models.CharField(max_length=255,verbose_name='表白内容') # 表白内容

    Cuser=models.ForeignKey('users.User',to_field="StudentID") # 关联用户

    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    is_anonymity = models.BooleanField(default=False,verbose_name='是否匿名') #是否匿名,默认不匿名

    is_delete=models.BooleanField(default=False,verbose_name='删除标记') # 逻辑删除


    # # 评论数
    # comment_count = models.IntegerField(verbose_name="评论数", default=0)
    # # 点赞数
    # up_count = models.IntegerField(verbose_name="点赞数", default=0)



    def __str__(self):
        return self.content


    class Meta:
        verbose_name = "表白墙"
        verbose_name_plural = verbose_name
        ordering=['-create_time'] # 按创建时间倒序

#
# class ConfessionImages(models.Model):
#
#     """
#     表白墙的照片
#     """
#
#     images = models.FileField(upload_to = "wall_imgs/",verbose_name="照片")
#
#     img_conn = models.ForeignKey(to="ConfessionWall", to_field="id")



class ConfessionImages(models.Model):

    """
    表白墙的照片
    """

    ImagesUrl = models.CharField(max_length=200,verbose_name="照片url")

    img_conn = models.ForeignKey(to="ConfessionWall", to_field="id")

    def __str__(self):
        return self.ImagesUrl

    class Meta:
        verbose_name = "表白墙照片"
        verbose_name_plural = verbose_name
