
from django.conf.urls import url
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('posts/search', views.POSTSearchViewSet, base_name='posts_search')



urlpatterns = [



    url(r'^posts/$', views.PostListView.as_view(),name='post-list'), # 展示贴子
    url(r'^post/$', views.PostCreateView.as_view(),name='post-create'), #　创建帖子
    url(r'^postr/(?P<pk>\d+)/$', views.PostViewSet.as_view(),name='post-detail'), #　详情帖子
    url(r'^delete/post/(?P<pk>\d+)/$', views.DelPostView.as_view()),  # 删除贴吧
    url(r"^likep/", views.LikeView.as_view),  # 赞  动态

]

urlpatterns += router.urls