
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^walls/$', views.WallListView.as_view()),

    url(r'^loves/$', views.CreateWallView.as_view()),
    url(r'^lovess/$', views.lovetest.as_view()),


]
