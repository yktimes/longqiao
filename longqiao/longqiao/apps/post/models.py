from django.db import models


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

    content = models.TextField(verbose_name="正文")

    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")

    category = models.ForeignKey(Category, verbose_name="分类", on_delete=models.DO_NOTHING)

    owner = models.ForeignKey('users.User', verbose_name="作者", on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "文章"
        ordering = ['-created_time']

    def __str__(self):
        return self.title
