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

# Create your views here.

class PostListView(ListAPIView):
    pass


class PostCreateView(CreateAPIView):

    serializer_class = CreatePostSerializer