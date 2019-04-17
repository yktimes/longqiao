
from django.conf.urls import url
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('posts/search', views.POSTSearchViewSet, base_name='posts_search')



urlpatterns = [



    url(r'^posts/$', views.PostListView.as_view()), #
    url(r'^post/$', views.PostCreateView.as_view()), #





]

urlpatterns += router.urls