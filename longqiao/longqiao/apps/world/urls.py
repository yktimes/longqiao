
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^walls/$', views.WallListView.as_view()),




]
