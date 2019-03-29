from django.db import models

# Create your models here.
class WorldCircle(models.Model):
    """
    世界圈
    """

    content = models.CharField(max_length=500,verbose_name='动态内容') # 动态内容

    Cuser=models.ForeignKey('users.User',to_field="StudentID") # 关联用户

    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")



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




class WorldImages(models.Model):

    """
    表白墙的照片
    """

    ImagesUrl = models.CharField(max_length=200,verbose_name="照片url")

    img_conn = models.ForeignKey(to="WorldCircle", to_field="id")

    def __str__(self):
        return self.ImagesUrl

    class Meta:
        verbose_name = "世界圈照片"
        verbose_name_plural = verbose_name



# class WorldComment(models.Model):
#     """
#     表白墙评论表
#     """
#     nid = models.AutoField(primary_key=True)
#     world = models.ForeignKey(to="WorldCircle", to_field="id")
#
#     # 外键，评论作者的 学号
#     author_id = models.ForeignKey(to='users.User',to_field="StudentID")
#
#     content = models.CharField(max_length=255)  # 评论内容
#
#     create_time = models.DateTimeField(auto_now_add=True)
#
#     parent_id = models.ForeignKey("self",related_name='parent', null=True, blank=True)  # blank=True 在django admin里面可以不填
#
#     def __str__(self):
#         return self.content
#     #
#     # def get_descendants(self):
#     #     '''获取一级评论的所有子孙'''
#     #     data = set()
#     #
#     #     def descendants(comment):
#     #         if comment.parent_id:
#     #             data.update(comment.parent_id)
#     #             for child in comment.parent_id:
#     #                 descendants(child)
#     #
#     #     descendants(self)
#     #     return data
#     #
#     #
#     # def to_dict(self):
#     #     data = {
#     #         'id': self.nid,
#     #         'body': self.content,
#     #         'timestamp': self.create_time,
#     #
#     #
#     #         'author': {
#     #             'id': self.author_id.StudentID,
#     #
#     #             'name': self.author_id.nickname,
#     #
#     #         },
#     #         'walls': {
#     #             'id': self.wall.id,
#     #             'title': self.wall.content,
#     #             'author_id': self.wall.Cuser.StudentID
#     #         },
#     #         'parent_id': self.parent_id if self.parent_id else None,
#     #         # 'children': [child.to_dict() for child in self.children] if self.children else None,
#     #
#     #     }
#     #     return data
#
#     class Meta:
#         verbose_name = "世界圈评论"
#         verbose_name_plural = verbose_name