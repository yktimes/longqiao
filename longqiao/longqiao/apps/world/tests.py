from django.test import TestCase

# Create your tests here.
# from django_redis import get_redis_connection
# from longqiao.apps.users.models import User

import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "longqiao.settings.dev")
django.setup()
from world.models import WallComment,ConfessionWall,ConfessionImages

import json
from fdfs_client.client import Fdfs_client

client = Fdfs_client('/home/python/longqiao/longqiao/longqiao/utils/fastdfs/client.conf')
import os,base64
if __name__ == '__main__':

    # url(r'^walls/$', views.BookListView.as_view()),


    from rest_framework.parsers import MultiPartParser, FileUploadParser, JSONParser

    # url(r'^loves/$', views.CreateWallView.as_view()),

    # class CreateWallView(CreateAPIView):
    #
    #     serializer_class = serializers.CreateConfessionWallSerializer
    #     parser_classes = (MultiPartParser, FileUploadParser,JSONParser)
    #     def get(self,request):
    #         return render(request, 'love.html')

    # 　使用 fastdfs
    strs="""
    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

    """
    imgdata = base64.b64decode(strs)
    print(imgdata)
    ret = client.upload_by_buffer(imgdata,file_ext_name='jpg')
    print(ret)
    print(ret)

    # def s():
    #     # 先获取一级评论
    #
    #     # 先获取一级评论
    #     data = WallComment.objects.filter(parent=None).order_by('create_time').first()
    #
    #     # 再添加子孙到一级评论的 descendants 属性上
    #     # for item in data['items']:
    #     #     comment = WallComment.objects.get(item['nid'])
    #     #     descendants = [child.to_dict() for child in comment.get_descendants()]
    #     #     # 按 timestamp 排序一个字典列表
    #     #     from operator import itemgetter
    #     #     item['descendants'] = sorted(descendants, key=itemgetter('create_time'))

    # def comments():
        # res = {'status': True, 'data': None, 'msg': None}
        # try:
        #     comment_list = WallComment.objects.filter(article_id=nid).values()
        #     com_list = list(comment_list)  # 所有的评论,列表套字典
        #     com_list_dict = {}  # 建立一个方便查找的数据结构字典
        #     for item in com_list:  # 循环评论列表,给每一条评论加一个child:[]就是让他装对他回复的内容
        #         item['create_time'] = str(item['create_time'])
        #         item['child'] = []
        #         com_list_dict[item['nid']] = item
        #     result = []
        #     for item in com_list:
        #         rid = item['reply_id']
        #         if rid:  # 如果reply_id不为空的话,那么就是说明他是子评论,我们要把他加入对应的评论后面
        #             com_list_dict[rid]['child'].append(item)
        #         else:
        #             result.append(item)
        #     print(result)
        #     # comment_str = comment_tree(result)
        #     # 这是在服务器上递归完之后,然后在传到前端,但是这样会增加服务器压力
        #     # 所以这种方式我们直接就不用了
        #     res['data'] = result
        # except Exception as e:
        #     res['status'] = False
        #     res['mag'] = str(e)
        # print(json.dumps(res))
        # # print(data.get_descendants())

    #     comment_list = WallComment.objects.filter(wall_id=1).values()
    #     ret = []  # 最终拿到的数据
    #     comment_list_dict = {}  # 构建的中间字典
    #     for row in comment_list:  # 通过查到的数据中的id作为key，每一行数据作为value生成一个字典
    #         row.update({"children": []})  # 构建一个键children对应一个空列表
    #         comment_list_dict[row["nid"]] = row  # 将id作为键，当前行作为值存到该字典中
    #
    #     for item in comment_list:  # 遍历一遍取到的数据列表
    #         parrent_row = comment_list_dict.get(item["parent_id_id"])  # 拿到当前行对应的父亲的地址
    #         if not parrent_row:  # 如果父亲是None，则直接进入ret中
    #             ret.append(item)
    #         else:  # 否则，将这行append到父亲的children中
    #             parrent_row["children"].append(item)  # 重点在这一行，用到了上面提到的第一个知识点
    #     print(ret)
    #     print(comment_list_dict)
    #
    # comments()

    # res = ConfessionWall.objects.filter(is_delete=False).values("id","content",'Cuser_id','Cuser__nickname')
    #
    # ret=[]
    #
    # wall_list_dict = {}  # 构建的中间字典
    # for row in res:
    #     row.update({"images":[]})
    #     s= ConfessionImages.objects.filter(img_conn=row["id"]).values("ImagesUrl")
    #     for i in s:
    #         row['images'].append(i['ImagesUrl'])
    # print(res)
    # print(p)
# from django.core.paginator import Paginator
# objects = ['john','paul','george','ringo','lucy','meiry','checy','wind','flow','rain']
# p = Paginator(objects,3)  # 3条数据为一页，实例化分页对象
# s = p.page(3)
# print(s.object_list)

    from django.db.models import Value

    # res = ConfessionImages.objects.annotate(s='img_conn__pk').select_related('img_conn','img_conn__Cuser').values('id',"ImagesUrl","img_conn__content","img_conn__create_time","img_conn__comment_count",'img_conn__up_count','img_conn__Cuser').values("")

    # res = ConfessionImages.objects.select_related('img_conn', 'img_conn__Cuser').annotate()
    # print(res)



