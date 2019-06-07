import base64

from django.shortcuts import render
from django.db.models import F
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.generics import CreateAPIView

from rest_framework.generics import DestroyAPIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView

from .serializers import PostListSerializer
from .serializers import CreatePostSerializer
from .serializers import POSTIndexSerializer
from .serializers import PostDetailSerializer
from .serializers import ImagesSerializer
from .models import Post
from . import constants
from fdfs_client.client import Fdfs_client

# Create your views here.
client = Fdfs_client(constants.FDFS)


class PostListView(ListAPIView):
    """
    帖子首页展示
    """
    # permission_classes = [IsAuthenticated]
    serializer_class = PostListSerializer

    # filter_backends = (OrderingFilter,)
    # ordering_fields = ('category')

    def get_queryset(self):
        return Post.all_posts()

    def filter_queryset(self, queryset):
        category_id = self.request.query_params.get("category")
        if category_id:
            return Post.objects.filter(category_id=category_id, status=Post.STATUS_NORMAL).select_related("Cuser",
                                                                                                          'category')

        return queryset


class PostCreateView(APIView):
    """
    新建贴吧
    """

    permission_classes = (IsAuthenticated,)  # 权限类,必须通过认证成功　才能访问或执行

    # def get(self, request):
    #
    #     return render(request, 'world.html')

    def post(self, request):

        print("user", request.user)
        print(request.data)

        images = request.data.getlist("images")

        # TODO　前段不传图片　出现问题
        if images == ['']:  # 如果图片为空
            print("lalallalallalallalal")
            images = None

        post = CreatePostSerializer(data=request.data)

        print(post, "sssssssssssss")

        if post.is_valid():  # 如果验证通过
            posts = post.save()  # 保存
            id = posts.pk  # 取到id
        else:

            return Response({'message': "标题和内容不能为空哦"}, status=status.HTTP_400_BAD_REQUEST)

        if images:  # 如果有图片
            print("图片个数", len(images))
            print("1111111111111111111111")
            for img in images:
                # if not isinstance(img, UploadedFile):  # 如果不是文件类型
                #     print("空的")
                #     del img  # 删除无效类型文件
                # else:
                #     print(img.name)
                try:
                    # ret = client.upload_by_buffer(img.read(), file_ext_name=img.name.split(".")[-1])

                    ret = client.upload_by_buffer(base64.b64decode(img), file_ext_name='jpg')
                    print(ret)
                    if ret["Status"] != "Upload successed.":
                        return Response({'message': "图片上传出错"}, status=status.HTTP_504_GATEWAY_TIMEOUT)
                except:

                    return Response({'message': "链接超时"}, status=status.HTTP_504_GATEWAY_TIMEOUT)
                else:
                    url = constants.StorageIP + ret["Remote file_id"]

                    pic = ImagesSerializer(data={'ImagesUrl': url, 'img_conn': id})

                    if pic.is_valid():
                        pic.save()

        return Response({"message": "ok"}, status=status.HTTP_200_OK)


class PostViewSet(RetrieveAPIView):
    """
    帖子详情
    """
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    serializer_class = PostDetailSerializer


class DelPostView(APIView):
    """
    删除贴吧
    """

    permission_classes = (IsAuthenticated,)  # 权限类,必须通过认证成功　才能访问或执行

    # delete/walls/<pk>/
    def post(self, request, pk):
        """
        处理删除
        """
        print(request.user)  # 可以得到用户
        try:
            post = Post.objects.get(id=pk, is_delete=False)

        except Post.DoesNotExist:
            return Response({'message': 'delete error'}, status=status.HTTP_400_BAD_REQUEST)
        else:

            # 如果删除用户是当前用户
            if post.Cuser == request.user:
                # 进行逻辑删除
                post.status = Post.STATUS_DELETE
                post.save()
                return Response({'message': 'delete ok'}, status=status.HTTP_204_NO_CONTENT)


class LikeView(APIView):
    """点赞"""
    permission_classes = [IsAuthenticated]

    def post(self, request):

        post_id = request.data['nid']

        try:
            news = Post.objects.get(pk=post_id)

        except Post.DoesNotExist:
            return Response({"message": "操作错误"})
        else:

            # 取消或添加赞
            news.switch_like(request.user)
            news.update(up_count=F("up_count") + 1)

            # return Response({"likes": news.count_likers()})
            return Response({"message": "ok"})


from drf_haystack.viewsets import HaystackViewSet


class POSTSearchViewSet(HaystackViewSet):
    """
    POST搜索
    """
    index_models = [Post]

    serializer_class = POSTIndexSerializer
