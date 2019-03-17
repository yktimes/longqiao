from django.shortcuts import render
from django.core.files.uploadedfile import UploadedFile

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.generics import CreateAPIView
from rest_framework import status

from .models import ConfessionWall
from . import constants
from . import serializers

from fdfs_client.client import Fdfs_client

# url(r'^walls/$', views.BookListView.as_view()),
class WallListView(ListAPIView):
    serializer_class = serializers.ConfessionWallSerializer

    def get_queryset(self):

        return ConfessionWall.objects.filter(is_delete=False)
from rest_framework.parsers import MultiPartParser,FileUploadParser,JSONParser

# url(r'^loves/$', views.CreateWallView.as_view()),

# class CreateWallView(CreateAPIView):
#
#     serializer_class = serializers.CreateConfessionWallSerializer
#     parser_classes = (MultiPartParser, FileUploadParser,JSONParser)
#     def get(self,request):
#         return render(request, 'love.html')

#　使用 fastdfs
client = Fdfs_client('longqiao/utils/fastdfs/client.conf')


class CreateWallView(APIView):
    """
    新建表白墙
    """

    def get(self, request):

        return render(request, 'love.html')

    def post(self,request):
        try:
            # 先接受下是否有图片,图片可以有多个
            images = request.data.getlist("images")
            #　验证表白墙数据
            wall = serializers.CreateConfessionWallSerializer(data=request.data)
            if wall.is_valid(): # 如果验证通过
                love_wall = wall.save() # 保存
                id = love_wall.pk # 取到表白墙id
            else:
                return Response({'message':"参数出错,无法创建"},status=status.HTTP_400_BAD_REQUEST)

            if images: # 如果有图片
                print(images)
                for img in images:
                    if not isinstance(img,UploadedFile):# 如果不是文件类型
                        print("空的")
                        del img # 删除无效类型文件
                    else:
                        print(img.name)
                        try:
                            ret = client.upload_by_buffer(img.read(),file_ext_name=img.name.split(".")[-1])
                            if ret["Status"]!="Upload successed.":
                                return Response({'message':"图片上传出错"},status=status.HTTP_504_GATEWAY_TIMEOUT)
                        except:
                            return Response({'message': "链接超时"},status=status.HTTP_504_GATEWAY_TIMEOUT)
                        else:
                            url = constants.StorageIP+ret["Remote file_id"]
                            pic = serializers.ConfessionImagesSerializer(data={'ImagesUrl':url,'img_conn':id})

                            if pic.is_valid():
                                pic.save()
        except:
            return Response({'message':"连接超时"},status=status.HTTP_504_GATEWAY_TIMEOUT)


        print(request.data)
        return Response({"message": "ok"},status=status.HTTP_200_OK)


# class WallListView(APIView):
#     def get(self, request):
#         wall = ConfessionWall.objects.all()
#
#
#         ids = []
#         for i in wall:
#             ids.append(i.pk)
#         serializer = serializers.ConfessionWallSerializer(wall, many=True)
#
#         s = ConfessionImages.objects.filter(img_conn__in=ids)
#
#         # print(s.images)
#         return Response(serializer.data)

class lovetest(APIView):


    def get(self,request):
        return render(request,'love.html')

    def post(self,request):
        print(request.data)

        return Response({"me":"ok"})