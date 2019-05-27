
from django.conf.urls import url
from . import views


urlpatterns = [



    url(r'^marklist/$', views.NotificationUnreadListView.as_view(), name='unread'),
    # TODO　slug　后面改为　pk
    url(r'^mark-as-read/<slug>/$', views.mark_as_read, name='mark_as_read'),
    url(r'^mark-all-as-read/$', views.mark_all_as_read, name='mark_all_read'),
    url('latest-notifications/', views.get_latest_notifications, name='latest_notifications'),
]

