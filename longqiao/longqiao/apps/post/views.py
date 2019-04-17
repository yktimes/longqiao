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

from rest_framework.filters import OrderingFilter

from .models import Post
# Create your views here.

class PostListView(ListAPIView):
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

class PostCreateView(CreateAPIView):

    serializer_class = CreatePostSerializer



from drf_haystack.viewsets import HaystackViewSet

class POSTSearchViewSet(HaystackViewSet):
    """
    POST搜索
    """
    index_models = [Post]

    serializer_class = POSTIndexSerializer