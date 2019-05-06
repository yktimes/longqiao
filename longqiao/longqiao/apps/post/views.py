from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.generics import CreateAPIView

from rest_framework.generics import DestroyAPIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from .serializers import PostListSerializer
from . serializers import CreatePostSerializer
from . serializers import  POSTIndexSerializer
from . serializers import  PostDetailSerializer
from rest_framework.filters import OrderingFilter

from .models import Post
# Create your views here.

class PostListView(ListAPIView):
    """
    帖子首页展示
    """
    serializer_class = PostListSerializer

    # filter_backends = (OrderingFilter,)
    # ordering_fields = ('category')

    def get_queryset(self):


        return Post.all_posts()

    def filter_queryset(self, queryset):

        category_id = self.request.query_params.get("category")
        if category_id:

            return Post.objects.filter(category_id=category_id, status=Post.STATUS_NORMAL).select_related("owner",'category')

        return queryset

from rest_framework.generics import RetrieveAPIView
class PostCreateView(CreateAPIView):
    """
    创建帖子
    """

    serializer_class = CreatePostSerializer

# class BookDetailView(RetrieveModelMixin, GenericAPIView):
#     queryset = BookInfo.objects.all()
#     serializer_class = BookInfoSerializer
#
#     def get(self, request, pk):
#         return self.retrieve(request)

class PostViewSet(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


from drf_haystack.viewsets import HaystackViewSet

class POSTSearchViewSet(HaystackViewSet):
    """
    POST搜索
    """
    index_models = [Post]

    serializer_class = POSTIndexSerializer