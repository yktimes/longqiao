from rest_framework_jwt.views import obtain_jwt_token
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^users/$', views.UserView.as_view()), # 创建用户

    url(r'^user/$', views.UserDetailView.as_view()), # 用户个人信息

    url(r'^info/$', views.UserUpdatelView.as_view()), # 修改用户个人信息
    # url(r'image_codes/$',views.ImageCodeView.as_view()),
    url(r'yz/$',views.Yz.as_view()),

    # url(r'^authorizations/$', obtain_jwt_token),


]
