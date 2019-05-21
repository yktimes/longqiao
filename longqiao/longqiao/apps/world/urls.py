from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^circle/$', views.CreateWorldView.as_view()),  # 创建动态(表白墙或世界圈)

    # url(r'^world/$', views.WorldListView.as_view()),  # 世界圈展示
    url(r'^world/$', views.WorldListView.as_view({'get': 'list'})),  # 世界圈展示
    url(r'^world/(?P<pk>\d+)/$', views.WorldListView.as_view({'get': 'retrieve'}), name='world-detail'),  # 世界圈详情展示

    url(r'^walls/$', views.WallListView.as_view({'get': 'list'})),  # 表白墙展示
    url(r'^walls/(?P<pk>\d+)/$', views.WallListView.as_view({'get': 'retrieve'}), name='walls-detail'),  # 表白墙详情展示

    url(r'^delete/walls/(?P<pk>\d+)/$', views.DelWallView.as_view()),  # 删除表白墙
    url(r'^delete/world/(?P<pk>\d+)/$', views.DelWorldView.as_view()),  # 删除动态

    url(r'^wallcomment/$', views.CreateWallCommentView.as_view()),  # 创建评论

    url(r'^wallcomments/$', views.WallCommentListView.as_view()),  # 得到评论
    url(r"^like/", views.LikeView.as_view), # 赞  动态
]
