
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^world/$', views.WorldListView.as_view()),  #　世界圈展示

    url(r'^circle/$', views.CreateWorldView.as_view()), # 创建动态
    #
    # url(r'^delete/walls/(?P<pk>\d+)/$', views.DelWallView.as_view()), # 删除表白墙
    #
    #
    #
    # url(r'^wallcomment/$', views.CreateWallCommentView.as_view()), # 创建评论
    #
    # url(r'^wallcomments/$', views.WallCommentListView.as_view()), # 得到评论





]

