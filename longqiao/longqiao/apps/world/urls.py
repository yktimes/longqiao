
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^walls/$', views.WallListView.as_view()),  #　表白墙展示

    url(r'^loves/$', views.CreateWallView.as_view()), # 创建表白墙

    url(r'^delete/walls/(?P<pk>\d+)/$', views.DelWallView.as_view()), # 删除表白墙



]

