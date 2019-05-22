from django.db import models
from django.core.cache import cache

# Create your models here.

class Category(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    CATEGORY_NORMAL = 0
    CATEGORY_STUDY = 1
    CATEGORY_COMPETITION = 2
    CATEGORY_LOSTANDFOUND = 3
    CATEGORY_SecondhandMarket = 4
    CATEGORY_DATA = 5
    CATEGORY_CARPOOLING = 6
    CATEGORY_GAME = 7
    CATEGORY_SHITS = 8



    CATEGORY_NAME =(
        (CATEGORY_STUDY,'学习天地'),
        (CATEGORY_COMPETITION,'竞赛组队'),
        (CATEGORY_LOSTANDFOUND,'失物招领'),
        (CATEGORY_SecondhandMarket,'二手市场'),
        (CATEGORY_DATA, '软件资料'),
        (CATEGORY_CARPOOLING,'我要拼车'),
        (CATEGORY_GAME,'游戏家'),
        (CATEGORY_SHITS,'吐槽'),

    )


    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    name = models.IntegerField(default=CATEGORY_NORMAL, choices=CATEGORY_NAME, verbose_name="分类名称")

    class Meta:
        verbose_name = verbose_name_plural = '分类'

    def __str__(self):
        return self.get_name_display()


class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0

    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),

    )

    title = models.CharField(max_length=255, verbose_name="标题")
    desc = models.CharField(max_length=255,verbose_name='摘要')
    content = models.TextField(verbose_name="正文")

    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")

    category = models.ForeignKey(Category, verbose_name="分类", on_delete=models.CASCADE)

    owner = models.ForeignKey('users.User', verbose_name="作者", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    liked = models.ManyToManyField('users.User', related_name='liked_post', verbose_name='点赞用户')

    # 评论数
    comment_count = models.IntegerField(verbose_name="评论数", default=0)
    # 点赞数
    up_count = models.IntegerField(verbose_name="点赞数", default=0)

    class Meta:
        verbose_name = verbose_name_plural = "文章"
        ordering = ['-created_time']

    def __str__(self):
        return self.title

    @classmethod
    def all_posts(cls):
        result = cache.get('all_posts') # 用到缓存
        if not result:
            result = cls.objects.filter(status=Post.STATUS_NORMAL).select_related("owner",'category')
            cache.set('all_posts', result, 60)
        return result



    def switch_like(self, user):
        """点赞或取消赞"""

        # 如果用户已经赞过，则取消赞
        if user in self.liked.all():
            self.liked.remove(user)

        else:
            self.liked.add(user)

    def count_likers(self):
        """点赞数"""
        return self.liked.count()

    def get_likers(self):
        """获取所有点赞用户"""
        return self.liked.all()
    # @classmethod
    # def category_posts(cls):
    #     result = cache.get('all_posts')
    #     if  result:
    #         result = result.
    #         cache.set('all_posts', result, 60)
    #     return result



class PostImages(models.Model):

    """
    贴吧的照片
    """

    ImagesUrl = models.CharField(max_length=200,verbose_name="照片url")

    img_conn = models.ForeignKey(to="Post", to_field="id")

    def __str__(self):
        return self.ImagesUrl

    class Meta:
        verbose_name = "贴吧照片"
        verbose_name_plural = verbose_name