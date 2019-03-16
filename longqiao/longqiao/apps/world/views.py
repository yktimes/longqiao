from django.shortcuts import render

# Create your views here.

from .models import ConfessionWall,ConfessionImages

from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers


from rest_framework.generics import ListAPIView


#
# class SKUListView(ListAPIView):
#     """
#     sku列表数据
#     """
#     serializer_class = SKUSerializer
#     filter_backends = (OrderingFilter,)
#     ordering_fields = ('create_time', 'price', 'sales')
#

# url(r'^walls/$', views.BookListView.as_view()),
class WallListView(ListAPIView):
    serializer_class = serializers.ConfessionWallSerializer

    def get_queryset(self):

        return ConfessionWall.objects.filter(is_delete=False)
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