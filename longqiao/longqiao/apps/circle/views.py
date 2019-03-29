from django.shortcuts import render
from django.core.files.uploadedfile import UploadedFile

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.generics import CreateAPIView

from rest_framework.generics import DestroyAPIView
from rest_framework import status
from rest_framework.mixins import DestroyModelMixin
from .models import WorldCircle,WorldImages

from rest_framework.permissions import IsAuthenticated
from . import serializers
from fdfs_client.client import Fdfs_client

from . import constants


# url(r'^walls/$', views.BookListView.as_view()),
class WorldListView(ListAPIView):
    serializer_class = serializers.WorldSerializer
    #permission_classes = (IsAuthenticated,)  # 权限类,必须通过认证成功　才能访问或执行

    def get_queryset(self):
        return WorldCircle.objects.filter(is_delete=False)


client = Fdfs_client(constants.FDFS)


# url(r'^loves/$', views.CreateWallView.as_view()),
class CreateWorldView(APIView):
    """
    新建世界圈
    """
    #permission_classes = (IsAuthenticated,)  # 权限类,必须通过认证成功　才能访问或执行

    def get(self, request):

        return render(request, 'world.html')

    def post(self, request):
        try:
            # 先接受下是否有图片,图片可以有多个
            images = request.data.getlist("images")
            # 　验证表白墙数据
            world = serializers.CreateWorldSerializer(data=request.data)
            if world.is_valid():  # 如果验证通过
                world_circle = world.save()  # 保存
                id = world_circle.pk  # 取到表白墙id
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
                            pic = serializers.WorldImagesSerializer(data={'ImagesUrl': url, 'img_conn': id})

                            if pic.is_valid():
                                pic.save()
        except:
            return Response({'message': "连接超时"}, status=status.HTTP_504_GATEWAY_TIMEOUT)

        print(request.data)
        return Response({"message": "ok"}, status=status.HTTP_200_OK)
