
from django.conf.urls import url
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('posts/search', views.POSTSearchViewSet, base_name='posts_search')



urlpatterns = [



    url(r'^posts/$', views.PostListView.as_view(),name='post-list'), # 展示贴子
    url(r'^post/$', views.PostCreateView.as_view(),name='post-create'), #　创建帖子
    url(r'^postr/(?P<pk>[0-9]+)/$', views.PostViewSet.as_view(),name='post-detail'), #　详情帖子





]

urlpatterns += router.urls