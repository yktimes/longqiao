from django.db import models
from longqiao.utils.models import BaseModel
# Create your models here.

class ConfessionWall(BaseModel):
    """
    表白墙
    """

    content = models.CharField(max_length=255) # 表白内容

    Cuser=models.ForeignKey('users.User',to_field="StudentID") # 关联用户

    is_anonymity = models.BooleanField(default=False) #是否匿名,默认不匿名

    is_delete=models.BooleanField(default=False) # 逻辑删除


    # # 评论数
    # comment_count = models.IntegerField(verbose_name="评论数", default=0)
    # # 点赞数
    # up_count = models.IntegerField(verbose_name="点赞数", default=0)



    def __str__(self):
        return self.content


    class Meta:
        verbose_name = "表白墙"
        verbose_name_plural = verbose_name


class ConfessionImages(models.Model):

    """
    表白墙的照片
    """

    images = models.FileField(upload_to = "wall_imgs/",verbose_name="照片")

    img_conn = models.ForeignKey(to="ConfessionWall", to_field="id")