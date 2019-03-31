from django.shortcuts import render
from django.core.files.uploadedfile import UploadedFile

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.generics import CreateAPIView

from rest_framework.generics import DestroyAPIView
from rest_framework import status
from rest_framework.mixins import DestroyModelMixin
from .models import ConfessionImages
from .models import  ConfessionWall
from .models import  WallComment


from .models import WorldImages
from .models import WorldCircle

from . import constants
from . import serializers
from rest_framework.permissions import IsAuthenticated



from fdfs_client.client import Fdfs_client

client = Fdfs_client(constants.FDFS)

# url(r'^walls/$', views.BookListView.as_view()),
class WallListView(ListAPIView):
    serializer_class = serializers.ConfessionWallSerializer
    #permission_classes = (IsAuthenticated,)  # 权限类,必须通过认证成功　才能访问或执行


    def get_queryset(self):

        res = ConfessionWall.objects.filter(is_delete=False).select_related('Cuser')

        return res
    # def get(self,request):
    #     from django.db.models import F
    #     res =  ConfessionWall.objects.filter(is_delete=False).select_related("Cuser",'confessionimages')
    #     print(res)
    #     s = serializers.ConfessionWallSerializer(res)
    #     print(s.data)
    #     return Response({'data':1})

    # def get_object(self):
    #     return ConfessionWall.objects.filter(is_delete=False).select_related("Cuser",'confessionimages').values("Cuser",'confessionimages')


from rest_framework.parsers import MultiPartParser, FileUploadParser, JSONParser

# url(r'^loves/$', views.CreateWallView.as_view()),

# class CreateWallView(CreateAPIView):
#
#     serializer_class = serializers.CreateConfessionWallSerializer
#     parser_classes = (MultiPartParser, FileUploadParser,JSONParser)
#     def get(self,request):
#         return render(request, 'love.html')

# 　使用 fastdfs  # 文件配置地址







class DelWallView(APIView):

    """
    删除表白墙
    """

    # authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)  # 权限类,必须通过认证成功　才能访问或执行

    # delete/walls/<pk>/
    def post(self, request, pk):
        """
        处理删除
        """
        print(request.user) # 可以得到用户
        try:
            wall = ConfessionWall.objects.get(id=pk, is_delete=False)
            if wall:
                # 进行逻辑删除
                wall.is_delete = True
                wall.save()
                return Response({'message': 'delete ok'}, status=status.HTTP_204_NO_CONTENT)
        except ConfessionWall.DoesNotExist:
            return Response({'message': 'delete error'}, status=status.HTTP_400_BAD_REQUEST)


#  url(r'^wallcomment/$', views.CreateWallCommentView.as_view()), # 创建评论
class CreateWallCommentView(CreateAPIView):

    #permission_classes = (IsAuthenticated,)  # 权限类,必须通过认证成功　才能访问或执行

    serializer_class = serializers.CreateWallCommentSerializer

    # def post(self,request):
    #     wall = request.POST.get("wall")
    #
    #     author_id = request.POST.get("author_id")
    #
    #     content = request.POST.get("content")
    #
    #     parent_id




class WallCommentListView(APIView):


    def get(self,request):
        comment_list = WallComment.objects.filter(wall_id=1).values('nid',
                                                                    'wall_id',
                                                                    "author_id_id",
                                                                    "author_id__nickname",
                                                                    "content",
                                                                    "create_time",
                                                                    "parent_id_id",


                                                                    )
        ret = []  # 最终拿到的数据
        comment_list_dict = {}  # 构建的中间字典
        for row in comment_list:  # 通过查到的数据中的id作为key，每一行数据作为value生成一个字典
            row.update({"children": []})  # 构建一个键children对应一个空列表
            comment_list_dict[row["nid"]] = row  # 将id作为键，当前行作为值存到该字典中

        for item in comment_list:  # 遍历一遍取到的数据列表
            parrent_row = comment_list_dict.get(item["parent_id_id"])  # 拿到当前行对应的父亲的地址
            if not parrent_row:  # 如果父亲是None，则直接进入ret中
                ret.append(item)
            else:  # 否则，将这行append到父亲的children中
                parrent_row["children"].append(item)  # 重点在这一行，用到了上面提到的第一个知识点
        print(ret)

        return Response({'comment':ret})
#
#         # 先获取一级评论
#         data = WallComment.objects.filter(parent=None).order_by('create_time')
#         # 再添加子孙到一级评论的 descendants 属性上
#         # for item in data['items']:
#         #     comment = WallComment.objects.get(item['nid'])
#         #     descendants = [child.to_dict() for child in comment.get_descendants()]
#         #     # 按 timestamp 排序一个字典列表
#         #     from operator import itemgetter
#         #     item['descendants'] = sorted(descendants, key=itemgetter('create_time'))
#
#         return Response({'data':data})

class WorldListView(ListAPIView):
    serializer_class = serializers.WorldSerializer

    #permission_classes = (IsAuthenticated,)  # 权限类,必须通过认证成功　才能访问或执行

    def get_queryset(self):
        return WorldCircle.objects.filter(is_delete=False).select_related("Cuser")



# url(r'^circle/$', views.CreateWorldView.as_view()),  # 创建动态(表白墙或世界圈)

class CreateWorldView(APIView):
    """
    新建动态
    """
    #permission_classes = (IsAuthenticated,)  # 权限类,必须通过认证成功　才能访问或执行

    def get(self, request):

        return render(request, 'world.html')

    def post(self, request):

        type = request.POST.get("type")
        try:
            # 先接受下是否有图片,图片可以有多个
            images = request.data.getlist("images")

            # 如果是世界圈类型
            if type==constants.WORLDCIRCLE:

                world = serializers.CreateWorldSerializer(data=request.data)

            # # 如果是表白墙类型
            if type==constants.LOVEWALL:
                world = serializers.CreateConfessionWallSerializer(data=request.data)


            if world.is_valid():  # 如果验证通过
                world_circle = world.save()  # 保存
                id = world_circle.pk  # 取到id

            else:
                return Response({'message': "参数出错,无法创建"}, status=status.HTTP_400_BAD_REQUEST)

            if images:  # 如果有图片
                print(images)
                for img in images:
                    if not isinstance(img, UploadedFile):  # 如果不是文件类型
                        print("空的")
                        del img  # 删除无效类型文件
                    else:
                        print(img.name)
                        try:
                            ret = client.upload_by_buffer(img.read(), file_ext_name=img.name.split(".")[-1])
                            if ret["Status"] != "Upload successed.":
                                return Response({'message': "图片上传出错"}, status=status.HTTP_504_GATEWAY_TIMEOUT)
                        except:
                            return Response({'message': "链接超时"}, status=status.HTTP_504_GATEWAY_TIMEOUT)
                        else:
                            url = constants.StorageIP + ret["Remote file_id"]


                            if type==constants.WORLDCIRCLE:
                                pic = serializers.WorldImagesSerializer(data={'ImagesUrl': url, 'img_conn': id})


                            if type==constants.LOVEWALL:
                                pic = serializers.ConfessionImagesSerializer(data={'ImagesUrl': url, 'img_conn': id})

                            if pic.is_valid():
                                pic.save()
        except:
            return Response({'message': "连接超时"}, status=status.HTTP_504_GATEWAY_TIMEOUT)

        print(request.data)
        return Response({"message": "ok"}, status=status.HTTP_200_OK)
