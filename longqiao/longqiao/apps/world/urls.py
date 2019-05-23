from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^circle/$', views.CreateWorldView.as_view()),  # 创建动态(表白墙或世界圈)


    # 首页
    url(r'^site/$', views.SiteListView.as_view({'get': 'list'})),  # 世界圈展示
    url(r'^site/(?P<pk>\d+)/$', views.SiteListView.as_view({'get': 'retrieve'}), name='site-detail'),

    # 置顶
    url(r'^top/site/$', views.TopListView.as_view()),  # 置顶展示
    url(r'^top/site/(?P<pk>\d+)/$', views.TopView.as_view()), # 置顶

    url(r'^f/$', views.FollowListView.as_view(), ), # 关注列表


    # 世界圈 动态
    url(r'^world/$', views.WorldListView.as_view({'get': 'list'})),  # 世界圈展示
    url(r'^world/(?P<pk>\d+)/$', views.WorldListView.as_view({'get': 'retrieve'}), name='world-detail'),  # 世界圈详情展示
    url(r'^delete/world/(?P<pk>\d+)/$', views.DelWorldView.as_view()),  # 删除动态

    # 表白墙
    url(r'^walls/$', views.WallListView.as_view({'get': 'list'})),  # 表白墙展示
    url(r'^walls/(?P<pk>\d+)/$', views.WallListView.as_view({'get': 'retrieve'}), name='walls-detail'),  # 表白墙详情展示
    url(r'^delete/walls/(?P<pk>\d+)/$', views.DelWallView.as_view()),  # 删除表白墙


    # 评论
    url(r'^wallcomment/$', views.CreateWallCommentView.as_view()),  # 创建评论

    url(r'^wallcomments/$', views.WallCommentListView.as_view()),  # 得到评论


    url(r"^like/", views.LikeView.as_view), # 赞  动态
]
