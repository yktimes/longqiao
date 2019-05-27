from django.db import models
from django.core.cache import cache
from longqiao.utils.models import BaseModel
from notifications.views import notification_handler

# Create your models here.
class Site(models.Model):
    """
    首页
    """

    content = models.TextField(verbose_name='首页内容') # 内容

    Cuser=models.ForeignKey('users.User',to_field="id") # 关联用户

    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    is_top = models.BooleanField(default=False,verbose_name = "是否置顶") # 是否置顶

    is_delete=models.BooleanField(default=False,verbose_name='删除标记') # 逻辑删除

    tag = models.CharField(max_length=30,null=True,blank=True,verbose_name="标签名称")

    liked = models.ManyToManyField('users.User', related_name='liked_site', verbose_name='点赞用户')
    # 评论数
    comment_count = models.IntegerField(verbose_name="评论数", default=0)
    # 点赞数
    up_count = models.IntegerField(verbose_name="点赞数", default=0)



    def __str__(self):
        return self.content


    class Meta:
        verbose_name = "首页"
        verbose_name_plural = verbose_name
        ordering=['-is_top','-create_time'] # 按创建时间倒序


    def switch_like(self, user):
        """点赞或取消赞"""

        # 如果用户已经赞过，则取消赞
        if user in self.liked.all():
            self.liked.remove(user)

        else:
            self.liked.add(user)

            # 添加赞的时候通知楼主　　# 这个ｋｅｙ可也不写
            # TODO　 首页点赞提醒
            # notification_handler(user,self.Cuser,'L',self,id_value=str(self.pk),key="social_update")

    def count_likers(self):
        """点赞数"""
        return self.liked.count()

    def get_likers(self):
        """获取所有点赞用户"""
        return self.liked.all()



    @classmethod
    def get_topped_sites(cls):
        """返回置顶"""
        # result = cache.get('top_sites')  # 用到缓存
        # if not result:
        #     topped_sites = cls.objects.filter(is_delete=False,is_top=True)
        #     cache.set('top_sites', topped_sites, 60*60*)
        #
        # return result

        topped_sites = cls.objects.filter(is_delete=False, is_top=True)
        return topped_sites


class SiteImages(models.Model):

    """
    首页的照片
    """

    ImagesUrl = models.CharField(max_length=200,verbose_name="照片url")

    img_conn = models.ForeignKey(to="Site", to_field="id")

    def __str__(self):
        return self.ImagesUrl

    class Meta:
        verbose_name = "首页照片"
        verbose_name_plural = verbose_name




class ConfessionWall(models.Model):
    """
    表白墙
    """

    content = models.CharField(max_length=255,verbose_name='表白内容') # 表白内容

    Cuser=models.ForeignKey('users.User',to_field="id") # 关联用户

    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    is_anonymity = models.BooleanField(default=False,verbose_name='是否匿名') #是否匿名,默认不匿名

    is_delete=models.BooleanField(default=False,verbose_name='删除标记') # 逻辑删除


    liked = models.ManyToManyField('users.User', related_name='liked_wall', verbose_name='点赞用户')
    # 评论数
    comment_count = models.IntegerField(verbose_name="评论数", default=0)
    # 点赞数
    up_count = models.IntegerField(verbose_name="点赞数", default=0)



    def __str__(self):
        return self.content


    class Meta:
        verbose_name = "表白墙"
        verbose_name_plural = verbose_name
        ordering=['-create_time'] # 按创建时间倒序

    def switch_like(self, user):
        """点赞或取消赞"""

        # 如果用户已经赞过，则取消赞
        if user in self.liked.all():
            self.liked.remove(user)

        else:
            self.liked.add(user)

            # 添加赞的时候通知楼主　　# 这个ｋｅｙ可也不写
                        # TODO　 表白墙点赞提醒
            # notification_handler(user,self.Cuser,'L',self,id_value=str(self.pk),key="social_update")


    def count_likers(self):
        """点赞数"""
        return self.liked.count()

    def get_likers(self):
        """获取所有点赞用户"""
        return self.liked.all()

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

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation



# class GenericDig(models.Model):
#     """通用点赞"""
#     nid = models.AutoField(primary_key=True)
#     # wall = models.ForeignKey(to="ConfessionWall", to_field="id")
#
#     # 外键，评论作者的 学号
#     author_id = models.ForeignKey(to='users.User', to_field="id")
#
#
#
#     create_time = models.DateTimeField(auto_now_add=True)
#
#
#     # GenericForeignKey设置
#     content_type = models.ForeignKey(ContentType, related_name='gen_comment', on_delete=models.CASCADE)
#     object_id = models.IntegerField()
#     digs = GenericForeignKey()
#
#     def __str__(self):
#         return self.author_id
#
#     class Meta:
#         verbose_name = '通用点赞'
#         verbose_name_plural = verbose_name
#
#         # SQL优化
#         index_together = ('content_type', 'object_id')  # 联合唯一索引
#
# class GenericComment(models.Model):
#     """
#     通用评论表
#     """
#     nid = models.AutoField(primary_key=True)
#     # wall = models.ForeignKey(to="ConfessionWall", to_field="id")
#
#     # 外键，评论作者的 学号
#     author_id = models.ForeignKey(to='users.User',to_field="id")
#
#     content = models.CharField(max_length=255)  # 评论内容
#
#     create_time = models.DateTimeField(auto_now_add=True)
#
#     parent_id = models.ForeignKey("self",related_name='parent', null=True, blank=True)  # blank=True 在django admin里面可以不填
#
#     # GenericForeignKey设置
#     content_type = models.ForeignKey(ContentType, related_name='gen_comment', on_delete=models.CASCADE)
#     object_id = models.CharField(max_length=255)
#     comments = GenericForeignKey()
#
#
#     def __str__(self):
#         return self.content
#
#     class Meta:
#         verbose_name = '通用评论'
#         verbose_name_plural = verbose_name
#
#         # SQL优化
#         index_together = ('content_type', 'object_id')  # 联合唯一索引


class WallComment(models.Model):
    """
    表白墙评论表
    """
    nid = models.AutoField(primary_key=True)
    wall = models.ForeignKey(to="ConfessionWall", to_field="id")

    # 外键，评论作者的 学号
    author_id = models.ForeignKey(to='users.User',to_field="id")

    content = models.CharField(max_length=255)  # 评论内容

    create_time = models.DateTimeField(auto_now_add=True)

    parent_id = models.ForeignKey("self",related_name='parent', null=True, blank=True)  # blank=True 在django admin里面可以不填

    def __str__(self):
        return self.content

    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #     super(WallComment,self).save()



    def get_descendants(self):
        '''获取一级评论的所有子孙'''
        data = set()

        def descendants(comment):
            if comment.parent_id:
                data.update(comment.parent_id)
                for child in comment.parent_id:
                    descendants(child)

        descendants(self)
        return data


    def to_dict(self):
        data = {
            'id': self.nid,
            'body': self.content,
            'timestamp': self.create_time,


            'author': {
                'id': self.author_id.StudentID,

                'name': self.author_id.nickname,

            },
            'walls': {
                'id': self.wall.id,
                'title': self.wall.content,
                'author_id': self.wall.Cuser.StudentID
            },
            'parent_id': self.parent_id if self.parent_id else None,
            # 'children': [child.to_dict() for child in self.children] if self.children else None,

        }
        return data

    class Meta:
        verbose_name = "表白墙评论"
        verbose_name_plural = verbose_name




class WorldCircle(models.Model):
    """
    世界圈
    """

    content = models.CharField(max_length=500,verbose_name='动态内容') # 动态内容

    Cuser=models.ForeignKey('users.User',to_field="id") # 关联用户

    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    liked = models.ManyToManyField('users.User', related_name='liked_world', verbose_name='点赞用户')


    is_delete=models.BooleanField(default=False,verbose_name='删除标记') # 逻辑删除


    # 评论数
    comment_count = models.IntegerField(verbose_name="评论数", default=0)
    # 点赞数
    up_count = models.IntegerField(verbose_name="点赞数", default=0)



    def __str__(self):
        return self.content


    class Meta:
        verbose_name = "世界圈"
        verbose_name_plural = verbose_name
        ordering=['-create_time'] # 按创建时间倒序




    def switch_like(self, user):
        """点赞或取消赞"""

        # 如果用户已经赞过，则取消赞
        if user in self.liked.all():
            self.liked.remove(user)

        else:
            self.liked.add(user)

            # 添加赞的时候通知楼主　　# 这个ｋｅｙ可也不写
            # TODO　 动态点赞提醒
            # notification_handler(user,self.Cuser,'L',self,id_value=str(self.pk),key="social_update")

    def count_likers(self):
        """点赞数"""
        return self.liked.count()

    def get_likers(self):
        """获取所有点赞用户"""
        return self.liked.all()


class WorldImages(models.Model):

    """
    世界圈照片
    """

    ImagesUrl = models.CharField(max_length=200,verbose_name="照片url")

    img_conn = models.ForeignKey(to="WorldCircle", to_field="id")

    def __str__(self):
        return self.ImagesUrl

    class Meta:
        verbose_name = "世界圈照片"
        verbose_name_plural = verbose_name