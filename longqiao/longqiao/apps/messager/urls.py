
from django.conf.urls import url
from . import views


urlpatterns = [



    url(r'^messages/$', views.MessagesListView.as_view(),name='messages_list'), # 展示消息列表
    url(r'^send-message/', views.Send_message.as_view(), name='send_message'),
    url(r'^m/(?P<pk>\d+)/', views.ConversationListView.as_view(), name='conversation_detail'),
]

